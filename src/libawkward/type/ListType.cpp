// BSD 3-Clause License; see https://github.com/jpivarski/awkward-1.0/blob/master/LICENSE

#include <string>
#include <sstream>

#include "awkward/array/ListOffsetArray.h"
#include "awkward/type/UnknownType.h"
#include "awkward/type/OptionType.h"

#include "awkward/type/ListType.h"

namespace awkward {
  ListType::ListType(const util::Parameters& parameters, const std::string& typestr, const std::shared_ptr<Type>& type)
      : Type(parameters, typestr)
      , type_(type) { }

  std::string ListType::tostring_part(const std::string& indent, const std::string& pre, const std::string& post) const {
    std::string typestr;
    if (get_typestr(typestr)) {
      return typestr;
    }

    std::stringstream out;
    if (parameters_.empty()) {
      out << indent << pre << "var * " << type_.get()->tostring_part(indent, "", "") << post;
    }
    else {
      out << indent << pre << "[var * " << type_.get()->tostring_part(indent, "", "") << ", " << string_parameters() << "]" << post;
    }
    return out.str();
  }

  const std::shared_ptr<Type> ListType::shallow_copy() const {
    return std::make_shared<ListType>(parameters_, typestr_, type_);
  }

  bool ListType::equal(const std::shared_ptr<Type>& other, bool check_parameters) const {
    if (ListType* t = dynamic_cast<ListType*>(other.get())) {
      if (check_parameters  &&  !parameters_equal(other.get()->parameters())) {
        return false;
      }
      return type().get()->equal(t->type(), check_parameters);
    }
    else {
      return false;
    }
  }

  int64_t ListType::numfields() const {
    return type_.get()->numfields();
  }

  int64_t ListType::fieldindex(const std::string& key) const {
    return type_.get()->fieldindex(key);
  }

  const std::string ListType::key(int64_t fieldindex) const {
    return type_.get()->key(fieldindex);
  }

  bool ListType::haskey(const std::string& key) const {
    return type_.get()->haskey(key);
  }

  const std::vector<std::string> ListType::keys() const {
    return type_.get()->keys();
  }

  const std::shared_ptr<Content> ListType::empty() const {
    Index64 offsets(1);
    offsets.ptr().get()[0] = 0;
    std::shared_ptr<Content> content = type_.get()->empty();
    return std::make_shared<ListOffsetArray64>(Identities::none(), parameters_, offsets, content);
  }

  const std::shared_ptr<Type> ListType::type() const {
    return type_;
  }
}
