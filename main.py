import sys, getopt
import json
import csv
import keyword_generator
import naver_search_ad_api as naver


def main(argv):

    try:
        opts, args = getopt.getopt(argv, "hei:o:s:", ["input=", "output=", "auth-file=", "extended"])
    except getopt.GetoptError:
        print('main.py -s <auth file> -i <input file> -o <output file>')
        sys.exit(2)

    auth_file_path = None
    input_file_path = None
    output_file_path = None
    include_hint_keywords = True

    for opt, arg in opts:
        if opt == '-h':
            print('main.py -s <auth file> -i <input file> -o <output file>')
            sys.exit()
        elif opt in ("-i", "--input"):
            input_file_path = arg
        elif opt in ("-o", "--output"):
            output_file_path = arg
        elif opt in ("-s", "--auth-file"):
            auth_file_path = arg
        elif opt in ("-e", "--extended"):
            include_hint_keywords = False

    print('Auth file path is', auth_file_path)
    if auth_file_path is None:
        print('Auth file must be specified.')
        sys.exit(2)

    print('Input file path is', input_file_path)
    if input_file_path is None:
        print('One input file must be specified.')
        sys.exit(2)

    input_array = []

    with open(input_file_path, newline='') as input_file:
        reader = csv.reader(input_file)
        for row in reader:
            strip = list(map(lambda elem: elem.strip(), row))
            input_array.append(strip)

    generated_keywords = keyword_generator.generate_keyword_permutations(input_array)

    with open(auth_file_path, newline='') as auth_file:
        auth = json.load(auth_file)
        naver_api = naver.API(auth['customerId'], auth['licenseKey'], auth['secretKey'])

    stats = naver_api.retrieve_relative_keyword_stats(generated_keywords, include_hint_keywords)

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
