import cPickle as pkl
import random
import os

# Note that dataset `MED` does not have `past` and `future` task
datasets = ['TACoS', 'MPII', 'MED']
levels = ['easy', 'hard']
splits = ['split_1', 'split_2', 'split_3']
contexts = ['past', 'present', 'future']
stage = ['train', 'val', 'test']


def get_questions(tasks, task_name, limit=5):
    '''
    `meta_tasks.pkl` format:
        d = task[dataset][level][split][context][stage]
        `d` is a list with elements (video_name, "question_name/question_id"),
        e.g., ("0006_Clerks_00.20.47.105-00.20.55.240", "0006_Clerks_00.20.47.634-00.20.53.605/0")
    For hard questions, ten candidates are provided, while for easy questions,
    four candidates are provided.

    `dataset_level.pkl` format:
        a dict with `key`=video_name, while `value` is a list
        which index in the *question_id* and each elements is a dict with key:
            'T': the question template, 'desc': annotation,
            'W*': the candidates, while 'W0' is the correct answer.
    '''
    print("sample question for task: "+task_name)
    for n in task_name.split('/'):
        tasks = tasks[n]
    question_pkl = '_'.join(task_name.split('/')[0: 2])
    with open(os.path.join('datasets', question_pkl+'.pkl')) as fin:
        question_pkl = pkl.load(fin)

    if 'hard' in task_name:
        num_candidate = 10
    else:
        num_candidate = 4
    example_counter = 0
    shuffled_tasks = list(tasks)
    random.shuffle(shuffled_tasks)
    for desc in shuffled_tasks:
        example_counter += 1
        video_id, question_ids = desc
        question_ids = question_ids.split('/')
        original_annotation = question_pkl[video_id]['desc']
        question_name = question_ids[0]
        question_idx = int(question_ids[1])
        question = question_pkl[question_name]['questions'][question_idx]
        candidates = ""
        for i in xrange(num_candidate):
            candidates += "{0}. {1}; ".format(i+1, question['W%d' % i])
        print("For video {0}\n"
              "\tannotation: {1}\n"
              "\tquestion template: {2}\n"
              "\tanswers: {3}".format(
                  video_id, original_annotation, question['T'], candidates))
        if example_counter == limit:
            return


def main():
    with open(os.path.join('datasets', 'meta_tasks.pkl')) as fin:
        print('loading task definition...')
        tasks = pkl.load(fin)
    get_questions(tasks, 'TACoS/easy/split_1/past/train')
    '''
    For video s23-d39_2_7
        annotation: The person washes the leeks in the sink.
        question template: the person cut off the _ then remove the outer sheaf of the leeks .
        answers: 1. root; 2. mango; 3. peach; 4. husk;
    '''
    # get_questions(tasks, 'TACoS/easy/split_2/present/val')
    # get_questions(tasks, 'TACoS/hard/split_3/future/test')
    # get_questions(tasks, 'MPII/easy/split_1/past/train')
    # get_questions(tasks, 'MPII/hard/split_2/present/val')
    # get_questions(tasks, 'MPII/easy/split_3/future/test')
    # get_questions(tasks, 'MED/hard/split_1/present/train')
    # get_questions(tasks, 'MED/easy/split_2/present/val')
    # get_questions(tasks, 'MED/easy/split_3/present/test')


if __name__ == "__main__":
    main()
