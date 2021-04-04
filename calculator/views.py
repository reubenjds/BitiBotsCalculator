from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, "input.html")

import random


class Bot:
    def __init__(self, eye, body, head, mouth, mental, generation, hashrate=None):
        self.eye = eye
        self.body = body
        self.head = head
        self.mouth = mouth
        self.mental = mental
        self.generation = generation
        self.hashrate = hashrate
        self.total = eye + body + head + mouth + mental
        self.fee = 0
        self.ap = 0

    def setHashrate(self, hashrate):
        self.hashrate = hashrate

    def AttributePoints(self):
        if self.eye <= 2:
            self.ap += 3
            self.apeye = 3
        elif self.eye <= 4:
            self.ap += 5
            self.apeye = 5
        else:
            self.ap += 8
            self.apeye = 8

        if self.body <= 4:
            self.ap += 1
            self.apbody = 1
        else:
            self.ap += 2
            self.apbody = 2

        if self.head <= 5:
            self.ap += 1
            self.aphead = 1
        else:
            self.ap += 2
            self.aphead = 2

        if self.mouth <= 6:
            self.ap += 1
            self.apmouth = 1
        else:
            self.ap += 2
            self.apmouth = 2

        if self.mental <= 7:
            self.ap += 1
            self.apmental = 1
        else:
            self.ap += 3
            self.apmental = 3

    def addAttributes(self, eye, body, head, mouth, mental):
        self.eye += eye
        self.body += body
        self.head += head
        self.mouth += mouth
        self.mental += mental

    def divideAttributes(self, num):
        self.eye //= num
        self.body //= num
        self.head //= num
        self.mouth //= num
        self.mental //= num
        self.ap //= num
    
    def get_hashrate(self):
        if p1.generation == p2.generation:
            hashrate = (p1.hashrate + p2.hashrate) * 0.6 + (self.ap * 3 ** (self.generation - 1))
        else:
            hashrate = min(p1.hashrate, p2.hashrate) * 0.6 + (self.ap * 3 ** (self.generation - 1))

    def __str__(self):
        return f" Eye Value is {self.eye}\n Body value is {self.body}\n Head value is {self.head}\n Mouth value is {self.mouth}\n Mental value is {self.mental}\n Attribute Total is {self.ap}"


def create_child(p1, p2):
    eye = p1.eye
    generation = min(p1.generation, p2.generation) + 1
    number = random.randint(1, 100)
    fee = generation * 1
    if number < 40:
        body = p1.body
    elif number < 80:
        body = p2.body
    elif number < 101:
        body = random.randint(0, 9)
    number = random.randint(1, 100)
    if number < 40:
        head = p1.head
    elif number < 80:
        head = p2.head
    elif number < 101:
        head = random.randint(0, 9)
    number = random.randint(1, 100)
    if number < 40:
        mouth = p1.mouth
    elif number < 80:
        mouth = p2.mouth
    elif number < 101:
        mouth = random.randint(0, 9)
    number = random.randint(1, 100)
    if number < 40:
        mental = p1.mental
    elif number < 80:
        mental = p2.mental
    elif number < 101:
        mental = random.randint(0, 9)
    mparent = min(p1.hashrate, p2.hashrate)
    child = Bot(eye, body, head, mouth, mental, generation)
    if p1.generation == p2.generation:
        child.setHashrate((p1.hashrate + p2.hashrate) * 0.6 + (child.ap * 3 ** (child.generation - 1)))
    else:
        child.setHashrate(mparent * 0.6 + (child.ap * 3 ** (child.generation - 1)))
    return child


def main(request):
    average = Bot(0, 0, 0, 0, 0, 0, 0)
    children = []
    p1 = Bot(int(request.POST['p1eye']), int(request.POST['p1body']), int(request.POST['p1head']), int(request.POST['p1mouth']), int(request.POST['p1mental']), int(request.POST['p1generation']), int(request.POST['p1hashrate']))
    p2 = Bot(int(request.POST['p1eye']), int(request.POST['p2body']), int(request.POST['p2head']), int(request.POST['p2mouth']), int(request.POST['p2mental']), int(request.POST['p2generation']), int(request.POST['p2hashrate']))
    for i in range(20000):
        children.append(create_child(p1, p2))
    for i in range(len(children)):
        average.addAttributes(children[i].eye, children[i].body, children[i].head, children[i].mouth,
                              children[i].mental)
    average.divideAttributes(len(children))
    average.AttributePoints()
    average.generation = min(p1.generation, p2.generation) + 1
    mparent = min(p1.hashrate, p2.hashrate)
    highest_total = children[0].total
    highest_i = 0
    for i in range(len(children)):
        if children[i].total > highest_total:
            highest_total = children[i].total
            highest_i = i
    children[highest_i].AttributePoints()
    children[highest_i].fee = children[highest_i].generation * 1
    if p1.generation == p2.generation:
        children[highest_i].setHashrate((p1.hashrate + p2.hashrate) * 0.6 + (children[highest_i].ap * 3 ** (children[highest_i].generation - 1)))
        average.setHashrate((p1.hashrate + p2.hashrate) * 0.6 + (average.ap * 3 ** (average.generation - 1)))
    else:
        children[highest_i].setHashrate(mparent * 0.6 + (children[highest_i].ap * 3 ** (children[highest_i].generation - 1)))
        average.setHashrate(mparent * 0.6 + (average.ap * 3 ** (average.generation - 1)))
    return render(request, "result.html", {"highesti" : children[highest_i], "average" : average})


