# search-ad-stats

각 키워드 군 끼리 2~(키워드 군의 개수)까지의 cartesian product 을 구한 후 이 조합별 permutation 을 조합한 이후 각각에 대해
NAVER에서 제공하는 연관키워드 통계 정보를 가져와 화면에 출력하거나 csv 형식으로 저장하기 위한 프로젝트다.

## Execution

```bash
python main.py -s <auth file> -i <input file> -o <output file>
```

## Authentication File for NAVER api

```json
{
  "customerId": 1,
  "licenseKey": "SEARCH ADVERTISER's Center Experience Zone [Tools > API Manager] Create API license",
  "secretKey": "SEARCH ADVERTISER's Center Experience Zone [Tools > API Manager] Create API license"
}
```

## input file

CSV format으로 만들며 각 행은 특정 주제를 가진 키워드 군을 의미한다. 각 키워드 군 끼리 2~(키워드 군의 개수)까지의 cartesian product 을 구한 후
이 조합별 permutation 을 조합한 이후 각각에 대한 NAVER에서 제공하는 연관키워드 통계 정보를 가져오게 된다.