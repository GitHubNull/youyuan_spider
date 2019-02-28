import redis
import json


pi = '192.168.1.12'
localhost = '127.0.0.1'
red = redis.Redis(host=pi, port=6379, decode_responses=True, db=0)

age_key_list = []
age_key_list_kv = {}

education_key_list = []
education_key_list_kv = {}

income_key_list = []
income_key_list_kv = {}


def pare_data(base_index, base, cnt):

    start_index = 0
    end_index = 0
    for i in range(0, cnt, 1):

        start_index = base_index + i * base
        end_index = base_index + (i + 1) * base

        r = red.lrange('yy:items', start_index, end_index)

        for item in r:
            item = json.loads(item)
            age = item['age']
            if age not in age_key_list:
                age_key_list.append(age)
                age_key_list_kv[age] = 1
            else:
                age_key_list_kv[age] += 1

            education = item['education']
            if education not in education_key_list:
                education_key_list.append(education)
                education_key_list_kv[education] = 1
            else:
                education_key_list_kv[education] += 1

            in_come = item['in_come']
            if in_come not in income_key_list:
                income_key_list.append(in_come)
                income_key_list_kv[in_come] = 1
            else:
                income_key_list_kv[in_come] += 1

    return end_index



if __name__ == '__main__':

    total = 964134
    base_index = 0


    # 10,0000
    base = 100000
    base_index = pare_data(base_index, base, 9)
    print('base_index:{}'.format(base_index))

    # 1,0000
    base = 10000
    base_index = pare_data(base_index, base, 6)
    print('base_index:{}'.format(base_index))

    # 1000
    base = 1000
    base_index = pare_data(base_index, base, 4)
    print('base_index:{}'.format(base_index))

    # 100
    base = 100
    base_index = pare_data(base_index, base, 1)

    # 10
    base = 10
    base_index = pare_data(base_index, base, 3)
    print('base_index:{}'.format(base_index))

    # 1
    base = 1
    base_index = pare_data(base_index, base, 4)
    print('base_index:{}'.format(base_index))

    f1 = open('年龄分布情况.csv', 'w')
    f1.write('年龄,数量\n')

    print('年龄分布情况.csv:')
    for k in age_key_list_kv:
        print('{}\t\t{}'.format(k, age_key_list_kv[k]))
        f1.write('{},{}\n'.format(k, age_key_list_kv[k]))
    f1.close()
    print('-'*80)

    f2 = open('教育分布情况.csv', 'w')
    f2.write('教育水平,数量\n')
    print('教育分布情况.csv：')
    for k in education_key_list_kv:
        print('{}\t\t{}'.format(k, education_key_list_kv[k]))
        f2.write('{},{}\n'.format(k, education_key_list_kv[k]))
    f2.close()
    print('-'*80)

    f3 = open('收入分布情况.csv', 'w')
    f3.write('收入收平,数量\n')
    print('收入分布情况.csv：')
    for k in income_key_list_kv:
        print('{}\t\t{}'.format(k, income_key_list_kv[k]))
        f3.write('{},{}\n'.format(k, income_key_list_kv[k]))
    f3.close()


