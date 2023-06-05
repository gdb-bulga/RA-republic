#include "bed.hpp"
#include <gtest/gtest.h>
#include <gmock/gmock.h>

using namespace biovoltron;
using ::testing::_;
using ::testing::Return;

// Mocking the dependencies
namespace biovoltron {
    namespace file_io {
        namespace core {
            struct MockHeader {};
            struct MockRecord {};
        }
    }
}

class TestBed : public ::testing::Test {
protected:
    void SetUp() override {
        // Create and assign mock objects to the corresponding classes
        bedHeader.header = &mockHeader;
        bedRecord.header = &mockHeader;
    }

    biovoltron::BedHeader bedHeader;
    biovoltron::BedRecord bedRecord;
    biovoltron::file_io::core::MockHeader mockHeader;
};

TEST_F(TestBed, BedHeaderTest) {
    // Add assertions for specific behavior of BedHeader
}

TEST_F(TestBed, BedRecordTest) {
    // Add assertions for specific behavior of BedRecord
}

// Add more tests if needed

int main(int argc, char** argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
