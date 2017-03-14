import sys, getopt
import csv
import keyword_generator
import naver_search_ad_api as naver


def main(argv):
    input_file_path = None
    output_file_path = None
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["input=", "output="])
    except getopt.GetoptError:
        print('main.py -i <input file> -o <output file>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('main.py -i <input file> -o <output file>')
            sys.exit()
        elif opt in ("-i", "--input"):
            input_file_path = arg
        elif opt in ("-o", "--output"):
            output_file_path = arg

    print('Input file path is ', input_file_path)
    if input_file_path is None:
        print('One input file must be specified.')
        sys.exit(2)

    input_array = []

    with open(input_file_path, newline='') as input_file:
        reader = csv.reader(input_file)
        for row in reader:
            strip = map(lambda elem: elem.strip(), row)
            input_array.append(strip)

    generated_keywords = keyword_generator.generate_keyword_permutations(input_array)

    stats = naver.retrieve_relative_keyword_stats(generated_keywords)

    if output_file_path is None:
        print(','.join(['연관키워드', '월간검색수(PC)', '월간검색수(Mobile)',
               '월평균클릭수(PC)', '월평균클릭수(Mobile)', '월평균클릭률(PC)', '월평균클릭률(Mobile)',
               '경쟁정도', '월평균노출 광고수']))

        for e in stats:
            print(','.join(str(v) for v in [e['relKeyword'],
                                            e['monthlyPcQcCnt'], e['monthlyMobileQcCnt'],
                                            e['monthlyAvePcClkCnt'], e['monthlyAveMobileClkCnt'],
                                            e['monthlyAvePcCtr'], e['monthlyAveMobileCtr'],
                                            e['compIdx'],
                                            e['plAvgDepth']]))
    else:
        with open(output_file_path, 'w', newline='', encoding='utf-8') as result_file:
            result_writer = csv.writer(result_file)
            result_writer.writerow([
                '연관키워드', '월간검색수(PC)', '월간검색수(Mobile)',
                '월평균클릭수(PC)', '월평균클릭수(Mobile)', '월평균클릭률(PC)', '월평균클릭률(Mobile)',
                '경쟁정도', '월평균노출 광고수'])

            for e in stats:
                result_writer.writerow([
                    e['relKeyword'],
                    e['monthlyPcQcCnt'], e['monthlyMobileQcCnt'],
                    e['monthlyAvePcClkCnt'], e['monthlyAveMobileClkCnt'],
                    e['monthlyAvePcCtr'], e['monthlyAveMobileCtr'],
                    e['compIdx'],
                    e['plAvgDepth']])


if __name__ == "__main__":
    main(sys.argv[1:])
