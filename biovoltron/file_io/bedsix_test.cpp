#include "bedsix.hpp"
#include <gtest/gtest.h>

// Test fixture for BedSixRecord
class BedSixRecordTest : public ::testing::Test {
protected:
  void SetUp() override {
    // Set up test data
    record1 = { "chr1", 100, 200, '+', "gene_type1", "gene_name1" };
    record2 = { "chr2", 300, 400, '-', "gene_type2", "gene_name2" };
  }

  biovoltron::BedSixRecord record1;
  biovoltron::BedSixRecord record2;
};

// Test BedSixRecord operator<=>
TEST_F(BedSixRecordTest, CompareOperator) {
  EXPECT_TRUE(record1 < record2);
  EXPECT_FALSE(record2 < record1);
}

// Test BedSixRecord conversion operator
TEST_F(BedSixRecordTest, ConversionOperator) {
  biovoltron::Interval interval1 = record1;
  biovoltron::Interval interval2 = record2;

  EXPECT_EQ(interval1.seqid, record1.seqid);
  EXPECT_EQ(interval1.start, record1.start);
  EXPECT_EQ(interval1.end, record1.end);
  EXPECT_EQ(interval1.strand, record1.strand);

  EXPECT_EQ(interval2.seqid, record2.seqid);
  EXPECT_EQ(interval2.start, record2.start);
  EXPECT_EQ(interval2.end, record2.end);
  EXPECT_EQ(interval2.strand, record2.strand);
}

// Test bedsixreader functions

// Mock function for split
template <typename Str>
std::vector<std::string> split(Str&& str, const std::string& delimiter) {
  std::vector<std::string> results;
  // Mock implementation
  // TODO: Implement mock behavior for split function
  return results;
}

// Mock function for read_mirtrondb_gff
template <typename Path>
void read_mirtrondb_gff(Path&& input_file_path, biovoltron::bedsixreader::bedsix_v& container) {
  // Mock implementation
  // TODO: Implement mock behavior for read_mirtrondb_gff function
}

// Mock function for read_mirbase_gff
template <typename Path>
void read_mirbase_gff(Path&& input_file_path, biovoltron::bedsixreader::bedsix_v& container) {
  // Mock implementation
  // TODO: Implement mock behavior for read_mirbase_gff function
}

// Mock function for read_gencode_gtf
template <typename Path>
void read_gencode_gtf(Path&& input_file_path, biovoltron::bedsixreader::bedsix_v& container) {
  // Mock implementation
  // TODO: Implement mock behavior for read_gencode_gtf function
}

// Test bedsixreader functions

// Test read_mirtrondb_gff
TEST(BedSixReaderTest, ReadMirtronDBGFF) {
  biovoltron::bedsixreader::bedsix_v container;
  // TODO: Prepare mock input file and call read_mirtrondb_gff function
  // Verify the results
}

// Test read_mirbase_gff
TEST(BedSixReaderTest, ReadMirbaseGFF) {
  biovoltron::bedsixreader::bedsix_v container;
  // TODO: Prepare mock input file and call read_mirbase_gff function
  // Verify the results
}

// Test read_gencode_gtf
TEST(BedSixReaderTest, ReadGencodeGTF) {
  biovoltron::bedsixreader::bedsix_v container;
  // TODO: Prepare mock input file and call read_gencode_gtf function
  // Verify the results
}

int main(int argc, char** argv) {
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
