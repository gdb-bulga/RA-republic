#include <googletest/gtest.h>
#include "fasta.hpp"

// Test fixture for FastaRecord
class FastaRecordTest : public ::testing::Test {
protected:
    void SetUp() override {
        // Set up test data
        record1.name = ">Seq1";
        record1.seq = "ACGT";
        record2.name = ">Seq2";
        record2.seq = "TGCA";
    }

    biovoltron::FastaRecord<false> record1;
    biovoltron::FastaRecord<false> record2;
};

// Predicate Coverage (PC) tests
TEST_F(FastaRecordTest, PC_Test) {
    // Check name
    ASSERT_EQ(record1.name, ">Seq1");
    ASSERT_EQ(record2.name, ">Seq2");

    // Check sequence
    ASSERT_EQ(record1.seq, "ACGT");
    ASSERT_EQ(record2.seq, "TGCA");
}

// Clause Coverage (CC) tests
TEST_F(FastaRecordTest, CC_Test) {
    // Check name
    ASSERT_EQ(record1.name, ">Seq1");
    ASSERT_EQ(record2.name, ">Seq2");

    // Check sequence
    ASSERT_EQ(record1.seq, "ACGT");
    ASSERT_EQ(record2.seq, "TGCA");

    // Check encoded flag
    ASSERT_FALSE(record1.encoded);
    ASSERT_FALSE(record2.encoded);
}

// Correlated Active Clause Coverage (CACC) tests
TEST_F(FastaRecordTest, CACC_Test) {
    // Check name
    ASSERT_EQ(record1.name, ">Seq1");
    ASSERT_EQ(record2.name, ">Seq2");

    // Check sequence
    ASSERT_EQ(record1.seq, "ACGT");
    ASSERT_EQ(record2.seq, "TGCA");

    // Check encoded flag
    ASSERT_FALSE(record1.encoded);
    ASSERT_FALSE(record2.encoded);

    // Check implicit conversion operator
    auto convertedRecord = static_cast<biovoltron::FastaRecord<true>>(record1);
    ASSERT_EQ(convertedRecord.name, ">Seq1");
    ASSERT_EQ(convertedRecord.seq, "ACGT");
    ASSERT_TRUE(convertedRecord.encoded);
}

// Test fixture for FastqRecord
class FastqRecordTest : public ::testing::Test {
protected:
    void SetUp() override {
        // Set up test data
        record1.name = "@Read1";
        record1.seq = "ACGT";
        record1.qual = "~~~~";
        record2.name = "@Read2";
        record2.seq = "TGCA";
        record2.qual = "####";
    }

    biovoltron::FastqRecord<false> record1;
    biovoltron::FastqRecord<false> record2;
};

// Predicate Coverage (PC) tests for FastqRecord
TEST_F(FastqRecordTest, PC_Test) {
    // Check name
    ASSERT_EQ(record1.name, "@Read1");
    ASSERT_EQ(record2.name, "@Read2");

    // Check sequence
    ASSERT_EQ(record1.seq, "ACGT");
    ASSERT_EQ(record2.seq, "TGCA");

    // Check quality
    ASSERT_EQ(record1.qual, "~~~~");
    ASSERT_EQ(record2.qual, "####");
}

// Clause Coverage (CC) tests for FastqRecord
TEST_F(FastqRecordTest, CC_Test) {
    // Check name
    ASSERT_EQ(record1.name, "@Read1");
    ASSERT_EQ(record2.name, "@Read2");

    // Check sequence
    ASSERT_EQ(record1.seq, "ACGT");
    ASSERT_EQ(record2.seq, "TGCA");

    // Check quality
    ASSERT_EQ(record1.qual, "~~~~");
    ASSERT_EQ(record2.qual, "####");

    // Check encoded flag
    ASSERT_FALSE(record1.encoded);
    ASSERT_FALSE(record2.encoded);
}

// Correlated Active Clause Coverage (CACC) tests for FastqRecord
TEST_F(FastqRecordTest, CACC_Test) {
    // Check name
    ASSERT_EQ(record1.name, "@Read1");
    ASSERT_EQ(record2.name, "@Read2");

    // Check sequence
    ASSERT_EQ(record1.seq, "ACGT");
    ASSERT_EQ(record2.seq, "TGCA");

    // Check quality
    ASSERT_EQ(record1.qual, "~~~~");
    ASSERT_EQ(record2.qual, "####");

    // Check encoded flag
    ASSERT_FALSE(record1.encoded);
    ASSERT_FALSE(record2.encoded);

    // Check implicit conversion operator
    auto convertedRecord = static_cast<biovoltron::FastqRecord<true>>(record1);
    ASSERT_EQ(convertedRecord.name, "@Read1");
    ASSERT_EQ(convertedRecord.seq, "ACGT");
    ASSERT_EQ(convertedRecord.qual, "~~~~");
    ASSERT_TRUE(convertedRecord.encoded);
}

// Test read operator for FastaRecord
TEST(FastaReadOperatorTest, ReadOperator_Test) {
    std::stringstream ss(">Seq1\nACGT\n>Seq2\nTGCA");
    biovoltron::FastaRecord<false> record1, record2;

    ASSERT_TRUE(ss >> record1);
    ASSERT_EQ(record1.name, ">Seq1");
    ASSERT_EQ(record1.seq, "ACGT");

    ASSERT_TRUE(ss >> record2);
    ASSERT_EQ(record2.name, ">Seq2");
    ASSERT_EQ(record2.seq, "TGCA");
}

// Test read operator for FastqRecord
TEST(FastqReadOperatorTest, ReadOperator_Test) {
    std::stringstream ss("@Read1\nACGT\n+\n~~~~\n@Read2\nTGCA\n+\n####");
    biovoltron::FastqRecord<false> record1, record2;

    ASSERT_TRUE(ss >> record1);
    ASSERT_EQ(record1.name, "@Read1");
    ASSERT_EQ(record1.seq, "ACGT");
    ASSERT_EQ(record1.qual, "~~~~");

    ASSERT_TRUE(ss >> record2);
    ASSERT_EQ(record2.name, "@Read2");
    ASSERT_EQ(record2.seq, "TGCA");
    ASSERT_EQ(record2.qual, "####");
}

// Test write operator for FastaRecord
TEST(FastaWriteOperatorTest, WriteOperator_Test) {
    std::stringstream ss;
    biovoltron::FastaRecord<false> record1;
    record1.name = ">Seq1";
    record1.seq = "ACGT";

    ss << record1;

    std::string expectedOutput = ">Seq1\nACGT";
    ASSERT_EQ(ss.str(), expectedOutput);
}

// Test write operator for FastqRecord
TEST(FastqWriteOperatorTest, WriteOperator_Test) {
    std::stringstream ss;
    biovoltron::FastqRecord<false> record1;
    record1.name = "@Read1";
    record1.seq = "ACGT";
    record1.qual = "~~~~";

    ss << record1;

    std::string expectedOutput = "@Read1\nACGT\n+\n~~~~";
    ASSERT_EQ(ss.str(), expectedOutput);
}

int main(int argc, char** argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
