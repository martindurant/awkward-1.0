// BSD 3-Clause License; see https://github.com/jpivarski/awkward-1.0/blob/master/LICENSE

#include <sstream>
#include <type_traits>

#include "awkward/cpu-kernels/identities.h"
#include "awkward/cpu-kernels/getitem.h"
#include "awkward/cpu-kernels/operations.h"
#include "awkward/type/OptionType.h"
#include "awkward/type/ArrayType.h"
#include "awkward/type/UnknownType.h"
#include "awkward/Slice.h"
#include "awkward/array/None.h"
#include "awkward/array/EmptyArray.h"
#include "awkward/array/UnionArray.h"
#include "awkward/array/NumpyArray.h"
#include "awkward/array/IndexedArray.h"
#include "awkward/array/ByteMaskedArray.h"
#include "awkward/array/BitMaskedArray.h"

#include "awkward/array/UnmaskedArray.h"

namespace awkward {
  UnmaskedArray::UnmaskedArray(const std::shared_ptr<Identities>& identities, const util::Parameters& parameters, const std::shared_ptr<Content>& content)
      : Content(identities, parameters)
      , content_(content) { }

  const std::shared_ptr<Content> UnmaskedArray::content() const {
    return content_;
  }

  const std::shared_ptr<Content> UnmaskedArray::project() const {
    return content_;
  }

  const std::shared_ptr<Content> UnmaskedArray::project(const Index8& mask) const {
    return std::make_shared<ByteMaskedArray>(Identities::none(), util::Parameters(), mask, content_, false).get()->project();
  }

  const Index8 UnmaskedArray::bytemask() const {
    Index8 out(length());
    struct Error err = awkward_zero_mask8(
      out.ptr().get(),
      length());
    util::handle_error(err, classname(), identities_.get());
    return out;
  }

  const std::shared_ptr<Content> UnmaskedArray::simplify_optiontype() const {
    if (dynamic_cast<IndexedArray32*>(content_.get())        ||
        dynamic_cast<IndexedArrayU32*>(content_.get())       ||
        dynamic_cast<IndexedArray64*>(content_.get())        ||
        dynamic_cast<IndexedOptionArray32*>(content_.get())  ||
        dynamic_cast<IndexedOptionArray64*>(content_.get())  ||
        dynamic_cast<ByteMaskedArray*>(content_.get())       ||
        dynamic_cast<BitMaskedArray*>(content_.get())        ||
        dynamic_cast<UnmaskedArray*>(content_.get())) {
      return content_;
    }
  }

  const std::shared_ptr<Content> UnmaskedArray::toIndexedOptionArray64() const {
    Index64 index(length());
    struct Error err = awkward_carry_arange_64(
      index.ptr().get(),
      length());
    util::handle_error(err, classname(), identities_.get());
    return std::make_shared<IndexedOptionArray64>(identities_, parameters_, index, content_);
  }

  const std::string UnmaskedArray::classname() const {
    return "UnmaskedArray";
  }

  void UnmaskedArray::setidentities(const std::shared_ptr<Identities>& identities) {
    if (identities.get() == nullptr) {
      content_.get()->setidentities(identities);
    }
    else {
      if (length() != identities.get()->length()) {
        util::handle_error(failure("content and its identities must have the same length", kSliceNone, kSliceNone), classname(), identities_.get());
      }
      if (Identities32* rawidentities = dynamic_cast<Identities32*>(identities.get())) {
        std::shared_ptr<Identities32> subidentities = std::make_shared<Identities32>(Identities::newref(), rawidentities->fieldloc(), rawidentities->width(), content_.get()->length());
        Identities32* rawsubidentities = reinterpret_cast<Identities32*>(subidentities.get());
        struct Error err = awkward_identities32_extend(
          rawsubidentities->ptr().get(),
          rawidentities->ptr().get(),
          rawidentities->offset(),
          rawidentities->length(),
          content_.get()->length());
        util::handle_error(err, classname(), identities_.get());
        content_.get()->setidentities(subidentities);
      }
      else if (Identities64* rawidentities = dynamic_cast<Identities64*>(identities.get())) {
        std::shared_ptr<Identities64> subidentities = std::make_shared<Identities64>(Identities::newref(), rawidentities->fieldloc(), rawidentities->width(), content_.get()->length());
        Identities64* rawsubidentities = reinterpret_cast<Identities64*>(subidentities.get());
        struct Error err = awkward_identities64_extend(
          rawsubidentities->ptr().get(),
          rawidentities->ptr().get(),
          rawidentities->offset(),
          rawidentities->length(),
          content_.get()->length());
        util::handle_error(err, classname(), identities_.get());
        content_.get()->setidentities(subidentities);
      }
      else {
        throw std::runtime_error("unrecognized Identities specialization");
      }
    }
    identities_ = identities;
  }

  void UnmaskedArray::setidentities() {
    if (length() <= kMaxInt32) {
      std::shared_ptr<Identities> newidentities = std::make_shared<Identities32>(Identities::newref(), Identities::FieldLoc(), 1, length());
      Identities32* rawidentities = reinterpret_cast<Identities32*>(newidentities.get());
      struct Error err = awkward_new_identities32(rawidentities->ptr().get(), length());
      util::handle_error(err, classname(), identities_.get());
      setidentities(newidentities);
    }
    else {
      std::shared_ptr<Identities> newidentities = std::make_shared<Identities64>(Identities::newref(), Identities::FieldLoc(), 1, length());
      Identities64* rawidentities = reinterpret_cast<Identities64*>(newidentities.get());
      struct Error err = awkward_new_identities64(rawidentities->ptr().get(), length());
      util::handle_error(err, classname(), identities_.get());
      setidentities(newidentities);
    }
  }

  const std::shared_ptr<Type> UnmaskedArray::type(const std::map<std::string, std::string>& typestrs) const {
    return std::make_shared<OptionType>(parameters_, util::gettypestr(parameters_, typestrs), content_.get()->type(typestrs));
  }

  const std::string UnmaskedArray::tostring_part(const std::string& indent, const std::string& pre, const std::string& post) const {
    std::stringstream out;
    out << indent << pre << "<" << classname() << ">\n";
    if (identities_.get() != nullptr) {
      out << identities_.get()->tostring_part(indent + std::string("    "), "", "\n");
    }
    if (!parameters_.empty()) {
      out << parameters_tostring(indent + std::string("    "), "", "\n");
    }
    out << content_.get()->tostring_part(indent + std::string("    "), "<content>", "</content>\n");
    out << indent << "</" << classname() << ">" << post;
    return out.str();
  }

  void UnmaskedArray::tojson_part(ToJson& builder) const {
    content_.get()->tojson_part(builder);
  }

  void UnmaskedArray::nbytes_part(std::map<size_t, int64_t>& largest) const {
    content_.get()->nbytes_part(largest);
  }

  int64_t UnmaskedArray::length() const {
    return content_.get()->length();
  }

  const std::shared_ptr<Content> UnmaskedArray::shallow_copy() const {
    return std::make_shared<UnmaskedArray>(identities_, parameters_, content_);
  }

  const std::shared_ptr<Content> UnmaskedArray::deep_copy(bool copyarrays, bool copyindexes, bool copyidentities) const {
    std::shared_ptr<Content> content = content_.get()->deep_copy(copyarrays, copyindexes, copyidentities);
    std::shared_ptr<Identities> identities = identities_;
    if (copyidentities  &&  identities_.get() != nullptr) {
      identities = identities_.get()->deep_copy();
    }
    return std::make_shared<UnmaskedArray>(identities, parameters_, content);
  }

  void UnmaskedArray::check_for_iteration() const {
    if (identities_.get() != nullptr  &&  identities_.get()->length() < length()) {
      util::handle_error(failure("len(identities) < len(array)", kSliceNone, kSliceNone), identities_.get()->classname(), nullptr);
    }
  }

  const std::shared_ptr<Content> UnmaskedArray::getitem_nothing() const {
    return content_.get()->getitem_range_nowrap(0, 0);
  }

  const std::shared_ptr<Content> UnmaskedArray::getitem_at(int64_t at) const {
    int64_t regular_at = at;
    if (regular_at < 0) {
      regular_at += length();
    }
    if (!(0 <= regular_at  &&  regular_at < length())) {
      util::handle_error(failure("index out of range", kSliceNone, at), classname(), identities_.get());
    }
    return getitem_at_nowrap(regular_at);
  }

  const std::shared_ptr<Content> UnmaskedArray::getitem_at_nowrap(int64_t at) const {
    return content_.get()->getitem_at_nowrap(at);
  }

  const std::shared_ptr<Content> UnmaskedArray::getitem_range(int64_t start, int64_t stop) const {
    int64_t regular_start = start;
    int64_t regular_stop = stop;
    awkward_regularize_rangeslice(&regular_start, &regular_stop, true, start != Slice::none(), stop != Slice::none(), length());
    if (identities_.get() != nullptr  &&  regular_stop > identities_.get()->length()) {
      util::handle_error(failure("index out of range", kSliceNone, stop), identities_.get()->classname(), nullptr);
    }
    return getitem_range_nowrap(regular_start, regular_stop);
  }

  const std::shared_ptr<Content> UnmaskedArray::getitem_range_nowrap(int64_t start, int64_t stop) const {
    std::shared_ptr<Identities> identities(nullptr);
    if (identities_.get() != nullptr) {
      identities = identities_.get()->getitem_range_nowrap(start, stop);
    }
    return std::make_shared<UnmaskedArray>(identities, parameters_, content_.get()->getitem_range_nowrap(start, stop));
  }

  const std::shared_ptr<Content> UnmaskedArray::getitem_field(const std::string& key) const {
    return std::make_shared<UnmaskedArray>(identities_, util::Parameters(), content_.get()->getitem_field(key));
  }

  const std::shared_ptr<Content> UnmaskedArray::getitem_fields(const std::vector<std::string>& keys) const {
    return std::make_shared<UnmaskedArray>(identities_, util::Parameters(), content_.get()->getitem_fields(keys));
  }

  const std::shared_ptr<Content> UnmaskedArray::getitem_next(const std::shared_ptr<SliceItem>& head, const Slice& tail, const Index64& advanced) const {
    if (head.get() == nullptr) {
      return shallow_copy();
    }
    else if (dynamic_cast<SliceAt*>(head.get())  ||  dynamic_cast<SliceRange*>(head.get())  ||  dynamic_cast<SliceArray64*>(head.get())  ||  dynamic_cast<SliceJagged64*>(head.get())) {
      UnmaskedArray out2(identities_, parameters_, content_.get()->getitem_next(head, tail, advanced));
      return out2.simplify_optiontype();
    }
    else if (SliceEllipsis* ellipsis = dynamic_cast<SliceEllipsis*>(head.get())) {
      return Content::getitem_next(*ellipsis, tail, advanced);
    }
    else if (SliceNewAxis* newaxis = dynamic_cast<SliceNewAxis*>(head.get())) {
      return Content::getitem_next(*newaxis, tail, advanced);
    }
    else if (SliceField* field = dynamic_cast<SliceField*>(head.get())) {
      return Content::getitem_next(*field, tail, advanced);
    }
    else if (SliceFields* fields = dynamic_cast<SliceFields*>(head.get())) {
      return Content::getitem_next(*fields, tail, advanced);
    }
    else if (SliceMissing64* missing = dynamic_cast<SliceMissing64*>(head.get())) {
      return Content::getitem_next(*missing, tail, advanced);
    }
    else {
      throw std::runtime_error("unrecognized slice type");
    }
  }

  const std::shared_ptr<Content> UnmaskedArray::carry(const Index64& carry) const {
    std::shared_ptr<Identities> identities(nullptr);
    if (identities_.get() != nullptr) {
      identities = identities_.get()->getitem_carry_64(carry);
    }
    return std::make_shared<UnmaskedArray>(identities, parameters_, content_.get()->carry(carry));
  }

  const std::string UnmaskedArray::purelist_parameter(const std::string& key) const {
    std::string out = parameter(key);
    if (out == std::string("null")) {
      return content_.get()->purelist_parameter(key);
    }
    else {
      return out;
    }
  }

  bool UnmaskedArray::purelist_isregular() const {
    return content_.get()->purelist_isregular();
  }

  int64_t UnmaskedArray::purelist_depth() const {
    return content_.get()->purelist_depth();
  }

  const std::pair<int64_t, int64_t> UnmaskedArray::minmax_depth() const {
    return content_.get()->minmax_depth();
  }

  const std::pair<bool, int64_t> UnmaskedArray::branch_depth() const {
    return content_.get()->branch_depth();
  }

  int64_t UnmaskedArray::numfields() const {
    return content_.get()->numfields();
  }

  int64_t UnmaskedArray::fieldindex(const std::string& key) const {
    return content_.get()->fieldindex(key);
  }

  const std::string UnmaskedArray::key(int64_t fieldindex) const {
    return content_.get()->key(fieldindex);
  }

  bool UnmaskedArray::haskey(const std::string& key) const {
    return content_.get()->haskey(key);
  }

  const std::vector<std::string> UnmaskedArray::keys() const {
    return content_.get()->keys();
  }

  const std::string UnmaskedArray::validityerror(const std::string& path) const {
    return content_.get()->validityerror(path + std::string(".content"));
  }

  const std::shared_ptr<Content> UnmaskedArray::shallow_simplify() const {
    return simplify_optiontype();
  }

  const std::shared_ptr<Content> UnmaskedArray::num(int64_t axis, int64_t depth) const {
    int64_t toaxis = axis_wrap_if_negative(axis);
    if (toaxis == depth) {
      Index64 out(1);
      out.ptr().get()[0] = length();
      return NumpyArray(out).getitem_at_nowrap(0);
    }
    else {
      return std::make_shared<UnmaskedArray>(Identities::none(), util::Parameters(), content_.get()->num(axis, depth));
    }
  }

  const std::pair<Index64, std::shared_ptr<Content>> UnmaskedArray::offsets_and_flattened(int64_t axis, int64_t depth) const {
    int64_t toaxis = axis_wrap_if_negative(axis);
    if (toaxis == depth) {
      throw std::invalid_argument("axis=0 not allowed for flatten");
    }
    else {
      std::pair<Index64, std::shared_ptr<Content>> offsets_flattened = content_.get()->offsets_and_flattened(axis, depth);
      Index64 offsets = offsets_flattened.first;
      std::shared_ptr<Content> flattened = offsets_flattened.second;
      if (offsets.length() == 0) {
        return std::pair<Index64, std::shared_ptr<Content>>(offsets, std::make_shared<UnmaskedArray>(Identities::none(), util::Parameters(), flattened));
      }
      else {
        return offsets_flattened;
      }
    }
  }

  bool UnmaskedArray::mergeable(const std::shared_ptr<Content>& other, bool mergebool) const {
    if (!parameters_equal(other.get()->parameters())) {
      return false;
    }

    if (dynamic_cast<EmptyArray*>(other.get())  ||
        dynamic_cast<UnionArray8_32*>(other.get())  ||
        dynamic_cast<UnionArray8_U32*>(other.get())  ||
        dynamic_cast<UnionArray8_64*>(other.get())) {
      return true;
    }

    if (IndexedArray32* rawother = dynamic_cast<IndexedArray32*>(other.get())) {
      return content_.get()->mergeable(rawother->content(), mergebool);
    }
    else if (IndexedArrayU32* rawother = dynamic_cast<IndexedArrayU32*>(other.get())) {
      return content_.get()->mergeable(rawother->content(), mergebool);
    }
    else if (IndexedArray64* rawother = dynamic_cast<IndexedArray64*>(other.get())) {
      return content_.get()->mergeable(rawother->content(), mergebool);
    }
    else if (IndexedOptionArray32* rawother = dynamic_cast<IndexedOptionArray32*>(other.get())) {
      return content_.get()->mergeable(rawother->content(), mergebool);
    }
    else if (IndexedOptionArray64* rawother = dynamic_cast<IndexedOptionArray64*>(other.get())) {
      return content_.get()->mergeable(rawother->content(), mergebool);
    }
    else if (ByteMaskedArray* rawother = dynamic_cast<ByteMaskedArray*>(other.get())) {
      return content_.get()->mergeable(rawother->content(), mergebool);
    }
    else if (BitMaskedArray* rawother = dynamic_cast<BitMaskedArray*>(other.get())) {
      return content_.get()->mergeable(rawother->content(), mergebool);
    }
    else if (UnmaskedArray* rawother = dynamic_cast<UnmaskedArray*>(other.get())) {
      return content_.get()->mergeable(rawother->content(), mergebool);
    }
    else {
      return content_.get()->mergeable(other, mergebool);
    }
  }

  const std::shared_ptr<Content> UnmaskedArray::reverse_merge(const std::shared_ptr<Content>& other) const {
    std::shared_ptr<Content> indexedoptionarray = toIndexedOptionArray64();
    IndexedOptionArray64* raw = dynamic_cast<IndexedOptionArray64*>(indexedoptionarray.get());
    return raw->reverse_merge(other);
  }

  const std::shared_ptr<Content> UnmaskedArray::merge(const std::shared_ptr<Content>& other) const {
    return toIndexedOptionArray64().get()->merge(other);
  }

  const std::shared_ptr<SliceItem> UnmaskedArray::asslice() const {
    return content_.get()->asslice();
  }

  const std::shared_ptr<Content> UnmaskedArray::rpad(int64_t target, int64_t axis, int64_t depth) const {
    int64_t toaxis = axis_wrap_if_negative(axis);
    if (toaxis == depth) {
      return rpad_axis0(target, false);
    }
    else if (toaxis == depth + 1) {
      return content_.get()->rpad(target, axis, depth);
    }
    else {
      return std::make_shared<UnmaskedArray>(Identities::none(), parameters_, content_.get()->rpad(target, axis, depth));
    }
  }

  const std::shared_ptr<Content> UnmaskedArray::rpad_and_clip(int64_t target, int64_t axis, int64_t depth) const {
    int64_t toaxis = axis_wrap_if_negative(axis);
    if (toaxis == depth) {
      return rpad_axis0(target, false);
    }
    else if (toaxis == depth + 1) {
      return content_.get()->rpad_and_clip(target, axis, depth);
    }
    else {
      return std::make_shared<UnmaskedArray>(Identities::none(), parameters_, content_.get()->rpad_and_clip(target, axis, depth));
    }
  }

  const std::shared_ptr<Content> UnmaskedArray::reduce_next(const Reducer& reducer, int64_t negaxis, const Index64& parents, int64_t outlength, bool mask, bool keepdims) const {
    return content_.get()->reduce_next(reducer, negaxis, parents, outlength, mask, keepdims);
  }

  const std::shared_ptr<Content> UnmaskedArray::localindex(int64_t axis, int64_t depth) const {
    int64_t toaxis = axis_wrap_if_negative(axis);
    if (axis == depth) {
      return localindex_axis0();
    }
    else {
      return std::make_shared<UnmaskedArray>(identities_, util::Parameters(), content_.get()->localindex(axis, depth));
    }
  }

  const std::shared_ptr<Content> UnmaskedArray::choose(int64_t n, bool diagonal, const std::shared_ptr<util::RecordLookup>& recordlookup, const util::Parameters& parameters, int64_t axis, int64_t depth) const {
    if (n < 1) {
      throw std::invalid_argument("in choose, 'n' must be at least 1");
    }
    int64_t toaxis = axis_wrap_if_negative(axis);
    if (axis == depth) {
      return choose_axis0(n, diagonal, recordlookup, parameters);
    }
    else {
      return std::make_shared<UnmaskedArray>(identities_, util::Parameters(), content_.get()->choose(n, diagonal, recordlookup, parameters, axis, depth));
    }
  }

  const std::shared_ptr<Content> UnmaskedArray::getitem_next(const SliceAt& at, const Slice& tail, const Index64& advanced) const {
    throw std::runtime_error("undefined operation: UnmaskedArray::getitem_next(at)");
  }

  const std::shared_ptr<Content> UnmaskedArray::getitem_next(const SliceRange& range, const Slice& tail, const Index64& advanced) const {
    throw std::runtime_error("undefined operation: UnmaskedArray::getitem_next(range)");
  }

  const std::shared_ptr<Content> UnmaskedArray::getitem_next(const SliceArray64& array, const Slice& tail, const Index64& advanced) const {
    throw std::runtime_error("undefined operation: UnmaskedArray::getitem_next(array)");
  }

  const std::shared_ptr<Content> UnmaskedArray::getitem_next(const SliceJagged64& jagged, const Slice& tail, const Index64& advanced) const {
    throw std::runtime_error("undefined operation: UnmaskedArray::getitem_next(jagged)");
  }

  const std::shared_ptr<Content> UnmaskedArray::getitem_next_jagged(const Index64& slicestarts, const Index64& slicestops, const SliceArray64& slicecontent, const Slice& tail) const {
    return getitem_next_jagged_generic<SliceArray64>(slicestarts, slicestops, slicecontent, tail);
  }

  const std::shared_ptr<Content> UnmaskedArray::getitem_next_jagged(const Index64& slicestarts, const Index64& slicestops, const SliceMissing64& slicecontent, const Slice& tail) const {
    return getitem_next_jagged_generic<SliceMissing64>(slicestarts, slicestops, slicecontent, tail);
  }

  const std::shared_ptr<Content> UnmaskedArray::getitem_next_jagged(const Index64& slicestarts, const Index64& slicestops, const SliceJagged64& slicecontent, const Slice& tail) const {
    return getitem_next_jagged_generic<SliceJagged64>(slicestarts, slicestops, slicecontent, tail);
  }

  template <typename S>
  const std::shared_ptr<Content> UnmaskedArray::getitem_next_jagged_generic(const Index64& slicestarts, const Index64& slicestops, const S& slicecontent, const Slice& tail) const {
    UnmaskedArray out2(identities_, parameters_, content_.get()->getitem_next_jagged(slicestarts, slicestops, slicecontent, tail));
    return out2.simplify_optiontype();
  }

}
