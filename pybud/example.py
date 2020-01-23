import time


def sample(a, b):
    """
    Test case 1
    """
    for _ in range(2):
        print("yes \n ")
        x = 8
        y = 14

        muted_variable_name = "This variable should be muted in the video output"

        x = a + b
        y = x * 2
        print('Math test: ' + str(y))

        friends = ['john', 'pat', 'gary', 'michael']
        for i in range(len(friends)):
            print("iteration {iteration} is {name}".format(iteration=i, name=friends[i]))

        muted_variable_name = "I, the muted variable, have changed"

        fl = 1.234

        a_string = "this is a string"
        print(a_string)
        numbers = [45, 67, 90, 2, 78]

        for j in range(len(numbers)):
            print("number: {}".format(numbers[j]))

        num_list = [100, 200, 700, 800]

        num_list.remove(200)

        dict_test = dict()

        dict_test["one"] = 2  # text wrapping test text wrapping test text wrapping test text wrapping test text wrapping test text wrapping test text wrapping test text wrapping test text wrapping test text wrapping test text wrapping test text wrapping test text wrapping test text wrapping test text wrapping test text wrapping test text wrapping test text wrapping test text wrapping test

        dict_test = {"one": 1, "two": 2}

        print("Test 2, test 3, Test the test?")

        dict_test = {"one": {"yes": "yes"}, "two": 2}

        dict_test["one"]["yes"] = 0


def nested_loop(a):
    """
        Test case 2
    """
    test_a = a

    num_list = [500, 600, 700]
    alpha_list = ['x', 'y', 'z']

    for number in num_list:
        print(number)
        time.sleep(1)
        for letter in alpha_list:
            print(letter)

    time.sleep(3.4)
