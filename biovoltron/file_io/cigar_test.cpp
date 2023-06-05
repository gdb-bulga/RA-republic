#include <googletest/googletest/gtest/gtest.h>
#include <biovoltron/file_io/cigar.hpp>

using namespace biovoltron;

TEST(CigarTest, ElementConversion) {
  Cigar::Element element{5, 'M'};
  std::string str_element = static_cast<std::string>(element);
  EXPECT_EQ(str_element, "5M");
}

TEST(CigarTest, ElementEquality) {
  Cigar::Element element1{5, 'M'};
  Cigar::Element element2{5, 'M'};
  Cigar::Element element3{6, 'M'};

  EXPECT_EQ(element1, element2);
  EXPECT_NE(element1, element3);
}

TEST(CigarTest, CigarConstructor) {
  Cigar cigar("3M2I4D");
  EXPECT_EQ(cigar.size(), 2);
}

TEST(CigarTest, CigarAssignment) {
  Cigar cigar;
  cigar = "3M2I4D";
  EXPECT_EQ(cigar.size(), 2);
}

TEST(CigarTest, CompactCigar) {
  Cigar cigar("3M2M4D");
  cigar.compact();
  EXPECT_EQ(cigar.size(), 2);
  EXPECT_EQ(cigar[0].size, 5);
  EXPECT_EQ(cigar[1].size, 4);
}

TEST(CigarTest, AccumulateRefSize) {
  Cigar cigar("3M2I4D");
  int ref_size = cigar.ref_size();
  EXPECT_EQ(ref_size, 7);
}

TEST(CigarTest, AccumulateReadSize) {
  Cigar cigar("3M2I4D");
  int read_size = cigar.read_size();
  EXPECT_EQ(read_size, 9);
}

TEST(CigarTest, AccumulateClipSize) {
  Cigar cigar("3M2I4D1S2H");
  int clip_size = cigar.clip_size();
  EXPECT_EQ(clip_size, 3);
}

TEST(CigarTest, CigarIteration) {
  Cigar cigar("3M2I4D");
  int count = 0;
  for (const auto& element : cigar) {
    count++;
  }
  EXPECT_EQ(count, cigar.size());
}

TEST(CigarTest, CigarToStringConversion) {
  Cigar cigar("3M2I4D");
  std::string str_cigar = static_cast<std::string>(cigar);
  EXPECT_EQ(str_cigar, "3M2I4D");
}

TEST(CigarTest, CigarPopFront) {
  Cigar cigar("3M2I4D");
  cigar.pop_front();
  EXPECT_EQ(cigar.size(), 1);
  EXPECT_EQ(cigar[0].size, 2);
}

TEST(CigarTest, CigarPopBack) {
  Cigar cigar("3M2I4D");
  cigar.pop_back();
  EXPECT_EQ(cigar.size(), 1);
  EXPECT_EQ(cigar[0].size, 3);
}

TEST(CigarTest, CigarReverse) {
  Cigar cigar("3M2I4D");
  cigar.reverse();
  EXPECT_EQ(cigar.size(), 2);
  EXPECT_EQ(cigar[0].size, 4);
  EXPECT_EQ(cigar[1].size, 3);
}

TEST(CigarTest, CigarContains) {
  Cigar cigar("3M2I4D");
  bool contains_M = cigar.contains('M');
  bool contains_I = cigar.contains('I');
  bool contains_D = cigar.contains('D');
  bool contains_S = cigar.contains('S');
  EXPECT_TRUE(contains_M);
  EXPECT_TRUE(contains_I);
  EXPECT_TRUE(contains_D);
  EXPECT_FALSE(contains_S);
}

TEST(CigarTest, EmptyCigar) {
  Cigar cigar;
  EXPECT_EQ(cigar.size(), 0);
  EXPECT_TRUE(cigar.empty());
}

TEST(CigarTest, CigarWithSingleElement) {
  Cigar cigar("5M");
  EXPECT_EQ(cigar.size(), 1);
  EXPECT_EQ(cigar[0].size, 5);
  EXPECT_EQ(cigar[0].operation, 'M');
}

TEST(CigarTest, CigarWithMultipleElements) {
  Cigar cigar("3M2I4D1S2H");
  EXPECT_EQ(cigar.size(), 4);
  EXPECT_EQ(cigar[0].size, 3);
  EXPECT_EQ(cigar[0].operation, 'M');
  EXPECT_EQ(cigar[1].size, 2);
  EXPECT_EQ(cigar[1].operation, 'I');
  EXPECT_EQ(cigar[2].size, 4);
  EXPECT_EQ(cigar[2].operation, 'D');
  EXPECT_EQ(cigar[3].size, 1);
  EXPECT_EQ(cigar[3].operation, 'S');
}

TEST(CigarTest, CigarFromStringConversion) {
  std::string str_cigar = "2I5M1D";
  Cigar cigar(str_cigar);
  std::string converted_cigar = static_cast<std::string>(cigar);
  EXPECT_EQ(converted_cigar, str_cigar);
}

TEST(CigarTest, CigarElementAccess) {
  Cigar cigar("3M2I4D");
  EXPECT_EQ(cigar.at(0).size, 3);
  EXPECT_EQ(cigar.at(0).operation, 'M');
  EXPECT_EQ(cigar[1].size, 2);
  EXPECT_EQ(cigar[1].operation, 'I');
}

TEST(CigarTest, CigarOutOfBoundsAccess) {
  Cigar cigar("3M2I4D");
  EXPECT_THROW(cigar.at(3), std::out_of_range);
}

TEST(CigarTest, CigarClear) {
  Cigar cigar("3M2I4D");
  EXPECT_FALSE(cigar.empty());
  cigar.clear();
  EXPECT_TRUE(cigar.empty());
}

TEST(CigarTest, CigarInsert) {
  Cigar cigar("3M2I4D");
  cigar.insert(cigar.begin() + 1, Cigar::Element{2, 'S'});
  EXPECT_EQ(cigar.size(), 4);
  EXPECT_EQ(cigar[1].size, 2);
  EXPECT_EQ(cigar[1].operation, 'S');
}

TEST(CigarTest, CigarErase) {
  Cigar cigar("3M2I4D");
  cigar.erase(cigar.begin() + 1);
  EXPECT_EQ(cigar.size(), 1);
  EXPECT_EQ(cigar[0].size, 3);
}

TEST(CigarTest, CigarSwap) {
  Cigar cigar1("3M2I4D");
  Cigar cigar2("2M1I3D");
  cigar1.swap(cigar2);
  EXPECT_EQ(cigar1.size(), 3);
  EXPECT_EQ(cigar1[0].size, 2);
  EXPECT_EQ(cigar1[1].size, 1);
  EXPECT_EQ(cigar1[2].size, 3);
  EXPECT_EQ(cigar2.size(), 2);
  EXPECT_EQ(cigar2[0].size, 3);
  EXPECT_EQ(cigar2[1].size, 4);
}

TEST(CigarTest, CigarEquality) {
  Cigar cigar1("3M2I4D");
  Cigar cigar2("3M2I4D");
  Cigar cigar3("2M1I3D");
  EXPECT_EQ(cigar1, cigar2);
  EXPECT_NE(cigar1, cigar3);
}

TEST(CigarTest, CigarCopyConstructor) {
  Cigar cigar1("3M2I4D");
  Cigar cigar2(cigar1);
  EXPECT_EQ(cigar2.size(), 2);
  EXPECT_EQ(cigar2[0].size, 3);
  EXPECT_EQ(cigar2[1].size, 4);
}

TEST(CigarTest, CigarMoveConstructor) {
  Cigar cigar1("3M2I4D");
  Cigar cigar2(std::move(cigar1));
  EXPECT_EQ(cigar2.size(), 2);
  EXPECT_EQ(cigar2[0].size, 3);
  EXPECT_EQ(cigar2[1].size, 4);
  EXPECT_TRUE(cigar1.empty());
}

TEST(CigarTest, CigarCopyAssignment) {
  Cigar cigar1("3M2I4D");
  Cigar cigar2;
  cigar2 = cigar1;
  EXPECT_EQ(cigar2.size(), 2);
  EXPECT_EQ(cigar2[0].size, 3);
  EXPECT_EQ(cigar2[1].size, 4);
}

TEST(CigarTest, CigarMoveAssignment) {
  Cigar cigar1("3M2I4D");
  Cigar cigar2;
  cigar2 = std::move(cigar1);
  EXPECT_EQ(cigar2.size(), 2);
  EXPECT_EQ(cigar2[0].size, 3);
  EXPECT_EQ(cigar2[1].size, 4);
  EXPECT_TRUE(cigar1.empty());
}

TEST(CigarTest, CigarReverseIterator) {
  Cigar cigar("3M2I4D");
  int count = 0;
  for (auto it = cigar.rbegin(); it != cigar.rend(); ++it) {
    count++;
  }
  EXPECT_EQ(count, cigar.size());
}

TEST(CigarTest, InvalidCigarInput) {
  // Test when an invalid cigar string is passed
  EXPECT_THROW({
    try {
      Cigar cigar("3M2X4D");  // 'X' is an invalid operation
    } catch (const std::exception& ex) {
      EXPECT_STREQ(ex.what(), "Invalid cigar operation: X");
      throw;
    }
  }, std::exception);

  // Test when an empty cigar string is passed
  EXPECT_THROW({
    try {
      Cigar cigar("");  // Empty cigar string
    } catch (const std::exception& ex) {
      EXPECT_STREQ(ex.what(), "Empty cigar string");
      throw;
    }
  }, std::exception);
}

TEST(CigarTest, EmptyCigar) {
  Cigar cigar;
  EXPECT_TRUE(cigar.empty());
  EXPECT_EQ(cigar.size(), 0);
}

TEST(CigarTest, MaxCigarSize) {
  // Test with a maximum allowed cigar size
  Cigar cigar("1000M");
  EXPECT_EQ(cigar.size(), 1);
  EXPECT_EQ(cigar[0].size, 1000);
}

TEST(CigarTest, MinCigarSize) {
  // Test with a minimum allowed cigar size
  Cigar cigar("1M");
  EXPECT_EQ(cigar.size(), 1);
  EXPECT_EQ(cigar[0].size, 1);
}

TEST(CigarTest, UnknownOperation) {
  // Test when an unknown operation is encountered
  Cigar cigar("3M2I4D9X");
  // Ensure that the unknown operation is skipped and not added to the cigar
  EXPECT_EQ(cigar.size(), 2);
  EXPECT_EQ(cigar[0].operation, 'M');
  EXPECT_EQ(cigar[1].operation, 'D');
}

// Add more tests to achieve desired coverage

int main(int argc, char** argv) {
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
