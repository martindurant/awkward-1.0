// BSD 3-Clause License; see https://github.com/jpivarski/awkward-1.0/blob/master/LICENSE

#ifndef AWKWARD_BOOLBUILDER_H_
#define AWKWARD_BOOLBUILDER_H_

#include "awkward/cpu-kernels/util.h"
#include "awkward/builder/ArrayBuilderOptions.h"
#include "awkward/builder/GrowableBuffer.h"
#include "awkward/builder/Builder.h"

namespace awkward {
  class EXPORT_SYMBOL BoolBuilder: public Builder {
  public:
    static const std::shared_ptr<Builder> fromempty(const ArrayBuilderOptions& options);

    BoolBuilder(const ArrayBuilderOptions& options, const GrowableBuffer<uint8_t>& buffer);

    const std::string classname() const override;
    int64_t length() const override;
    void clear() override;
    const std::shared_ptr<Content> snapshot() const override;

    bool active() const override;
    const std::shared_ptr<Builder> null() override;
    const std::shared_ptr<Builder> boolean(bool x) override;
    const std::shared_ptr<Builder> integer(int64_t x) override;
    const std::shared_ptr<Builder> real(double x) override;
    const std::shared_ptr<Builder> string(const char* x, int64_t length, const char* encoding) override;
    const std::shared_ptr<Builder> beginlist() override;
    const std::shared_ptr<Builder> endlist() override;
    const std::shared_ptr<Builder> begintuple(int64_t numfields) override;
    const std::shared_ptr<Builder> index(int64_t index) override;
    const std::shared_ptr<Builder> endtuple() override;
    const std::shared_ptr<Builder> beginrecord(const char* name, bool check) override;
    const std::shared_ptr<Builder> field(const char* key, bool check) override;
    const std::shared_ptr<Builder> endrecord() override;
    const std::shared_ptr<Builder> append(const std::shared_ptr<Content>& array, int64_t at) override;

  private:
    const ArrayBuilderOptions options_;
    GrowableBuffer<uint8_t> buffer_;
  };
}

#endif // AWKWARD_BOOLBUILDER_H_
