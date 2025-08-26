from firebase_config import get_databases
import numpy as np


def calculate_average(sentiment_scores):
    result = {}
    for keyword, scores in sentiment_scores.items():
        positive_scores = [score for score in scores if score > 0]
        negative_scores = [score for score in scores if score < 0]
        result[keyword] = {
            'average_positive': np.mean(positive_scores) if positive_scores else 0,
            'average_negative': np.mean(negative_scores) if negative_scores else 0
        }
    return result


def analyze_sentiment_scores(keywords):
    dbs = get_databases()
    sentiment_scores = {keyword.lower(): [] for keyword in keywords}
    print(f"Start parsing comments")

    for db_name, db_ref in dbs.items():
        comments_ref = db_ref.child('comments').get()
        if not comments_ref:
            print(f"No comments found from {db_name}.")
            return None

        for data_att, data_dict in comments_ref.items():
            if 'title' in data_dict and 'sentiment_score' in data_dict:
                for keyword in keywords:
                    if keyword in data_dict['title']:
                        keyword = keyword.lower()
                        sentiment_score = data_dict['sentiment_score']

                        if keyword in sentiment_scores:
                            sentiment_scores[keyword].append(sentiment_score)

    return sentiment_scores


def calculate_percentage_difference(sentiment_scores):
    averages = calculate_average(sentiment_scores)

    # Calculate total average for each keyword of interest
    trump_avg = averages['trump']['average_positive'] + abs(averages['biden']['average_negative'])
    biden_avg = averages['biden']['average_positive'] + abs(averages['trump']['average_negative'])
    republican_avg = averages['republican']['average_positive'] + abs(averages['democrat']['average_negative'])
    democrat_avg = averages['democrat']['average_positive'] + abs(averages['republican']['average_negative'])

    # print('---Trump avg: ', trump_avg,'---')
    # print('---Biden avg: ', biden_avg,'---')
    # print('---Republican avg: ', republican_avg,'---')
    # print('---Democrat avg: ', democrat_avg,'---')

    # Calculate average total
    candidate_total_avg = trump_avg + biden_avg
    parties_total_avg = republican_avg + democrat_avg

    # print('---Candidate total: ', candidate_total_avg, '---')
    # print('---Party total: ', parties_total_avg, '---')

    if trump_avg == 0:
        trump_ratio = 0
    else:
        trump_ratio = trump_avg / candidate_total_avg

    if biden_avg == 0:
        biden_ratio = 0
    else:
        biden_ratio = biden_avg / candidate_total_avg

    if republican_avg == 0:
        republican_ratio = 0
    else:
        republican_ratio = republican_avg / parties_total_avg

    if democrat_avg == 0:
        democrat_ratio = 0
    else:
        democrat_ratio = democrat_avg / parties_total_avg

    # print('---Trump ratio: ', trump_ratio*100, '%---')
    # print('---Biden ratio: ', biden_ratio*100, '%---')
    # print('---Republican ratio: ', republican_ratio*100, '%---')
    # print('---Democrat ratio: ', democrat_ratio*100, '%---')

    trump_total = (trump_ratio + republican_ratio)/2*100
    biden_total = (biden_ratio + democrat_ratio)/2*100

    # print('---Trump Total: ', trump_total, '%---')
    # print('---Biden Total: ', biden_total, '%---')

    # Check Winner and Difference
    if trump_total > biden_total:
        winner = "Trump"
        difference = round(trump_total - biden_total, 2)
    elif trump_total < biden_total:
        winner = "Biden"
        difference = round(biden_total - trump_total, 2)
    else:
        winner = "Tie"
        difference = 0

    print(f"{winner} is winning by {difference}%")

    return [winner, f"{difference}%"]


if __name__ == "__main__":
    keyword_to_search = ['Trump', 'Biden', 'Republican', 'Democrat']
    sentiment_scores = analyze_sentiment_scores(keyword_to_search)
    calculate_average(sentiment_scores)
    print('----------Calculating Who is winning----------')
    print(calculate_percentage_difference(sentiment_scores))
