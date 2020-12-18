import logging

# Create a custom logger
import os
import datetime
# util file must be placed in root


def get_filelogger(name,  filepath = 'file.log'):
    logger = logging.getLogger(name)
    if not len(logger.handlers):
        f_handler = logging.FileHandler(filepath)
        f_handler.setLevel(logging.INFO)
        f_format = logging.Formatter('%(asctime)s  - %(name)s - %(processName)s - %(threadName)s - %(levelname)s - %(message)s')
        f_handler.setFormatter(f_format)
        logger.addHandler(f_handler)
        logger.setLevel(logging.INFO)
    return logger


def get_logger(name):
    logger = logging.getLogger(name)
    # Create handlers
    if not len(logger.handlers):
        c_handler = logging.StreamHandler()
        c_handler.setLevel(logging.INFO)
        c_format = logging.Formatter('%(asctime)s  - %(name)s - %(processName)s - %(threadName)s - %(levelname)s - %(message)s')
        c_handler.setFormatter(c_format)
        logger.addHandler(c_handler)
        logger.setLevel(logging.INFO)
    return logger


def get_full_path(*args):
    """get the absolute path of file relative to root/utils file

    Args:
        args (str): string paths to join to make an absolute path

    Returns:
        str: full absolute path
    """

    ROOT_PATH = __file__
    ROOT_DIR  = os.path.dirname(ROOT_PATH)
    abs_path = os.path.join(ROOT_DIR, *args)
    abs_path = os.path.abspath(abs_path)

    return abs_path


def get_model_path(task_name, model_name, model_dir='../models', checkpoint=True, epoch=1, val_acc=0.9):

    if checkpoint == True:
        model_file_name = f'cp-{model_name}-{epoch}-{val_acc}.ckpt'
    else:
        model_file_name =  model_name
    model_dir = get_full_path(model_dir, task_name, model_file_name)

    return model_dir


def get_model_serving_path(task_name, model_name, serving_dir='models'):

    serving_path= get_full_path(serving_dir, task_name, model_name )

    return serving_path


def get_checkpoint_path(task_name, model_name, model_dir='models'):
    checkpoint_variables = '{epoch:02d}-{val_acc:.2f}'
    save_directory = get_full_path(model_dir, task_name)
    checkpoint_path = f"{save_directory}/cp-{model_name}-{checkpoint_variables}.ckpt"
    return checkpoint_path


def get_tensorboard_log_path(task_name,model_dir='models'):
    run_time =  datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    log_path  = get_full_path(model_dir, task_name, "logs", run_time)
    return log_path


def generate_batches(nexamples, batch_size):
    """generates a list of tuples of starts and ends of size nbatches

    Args:
        nexamples(int):
        batch_size(int):

    Returns:
        list: a list of tuples with start and end index of each batch

    """

    nbatches = int(np.ceil(nexamples / batch_size))
    batches = []
    for batch in range(nbatches):
        start = batch * batch_size
        end = start + batch_size

        if end > nexamples:
            end = nexamples

        batches.append((start, end))

    return batches


def get_datetime():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def divisorGenerator(n):
    large_divisors = []
    for i in range(1, int(np.sqrt(n) + 1)):
        if n % i == 0:
            yield i
            if i*i != n:
                large_divisors.append(int(n / i))
    for divisor in reversed(large_divisors):
        yield divisor


def getBatchsize(nexamples, selectedBatchSize, lowerBound = True):
    """return the batchsize which is exactly divisible by the number of examples an is closest to the proposed batchsize

    Args:
        nexamples(int):
        selectedBatchSize(int):
        lowerBound(bool):

    Returns:
        int: a closet divisible batchsize

    """

    divisors  = list(divisorGenerator(nexamples))[1:-1]

    if len(divisors) == 0:
        if lowerBound==True:
            return 1
        else:
            return nexamples

    previousDivisor = divisors[0]
    for divisor in divisors:
        if selectedBatchSize < divisor:
            if lowerBound == True:
                return previousDivisor
            else:
                return divisor
        previousDivisor = divisor

# get_model_path("gender_IN_jabong", "resnet50", epoch=10, val_acc=0.93)