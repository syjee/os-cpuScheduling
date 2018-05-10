class DNode:
    def __init__(self,id,turn_around_time,computing_time,queue_time = None,current_computing_time=None,prev=None, next=None):
        self.id = id
        self.computing_time = computing_time
        self.current_computing_time = computing_time
        self.turn_around_time = turn_around_time
        self.queue_time = 1
        self.arrival = turn_around_time
        self.finish = None

        self.prev = prev
        self.next = next

class List:
    def __init__(self, t):
        self.head_node = DNode(None, None, None, None, None)
        self.last_node = DNode(None, None, None, None, None)

        self.head_node.next = self.last_node
        self.last_node.prev = self.head_node
        self.queue_time = t

    def burst(self):
        node = self.head_node.next
        node.current_computing_time -= 1
        node.queue_time -= 1

    def print_node(self,node):
        global Tr,Normalize
        Tr += float(node.finish - node.arrival)
        Normalize += float(node.finish - node.arrival)/node.computing_time
        tat = node.finish-node.arrival
        nor_tat = float(float(node.finish - node.arrival)/node.computing_time)
        print(str(node.id) + "\t" + str(node.arrival) + "\t" + str(node.computing_time) +"\t"+str(node.finish)+"\t"+str(tat)+"\t"+'%.2f'%nor_tat)

    def insert_node(self,new_node):

        new_node.next = self.last_node
        new_node.prev = self.last_node.prev
        self.last_node.prev.next = new_node
        self.last_node.prev = new_node

    def delete_node(self,del_node):
        if (del_node == self.head_node):
            return
        del_node.prev.next = del_node.next
        del_node.next.prev = del_node.prev

        #del del_node

    def getListLen(self):
        len = 0
        node = self.head_node.next

        while node != self.last_node:
            len += 1
            node = node.next

        return len

    def print_list(self):
        node = self.head_node.next
        print("------------------------------------------------------------------")
        print("id\t\tcomputing_time\t\t\tturn_around_time\t")
        print("------------------------------------------------------------------")
        while node != self.last_node:
            self.print_node(node)
            node = node.next
        print("------------------------------------------------------------------")

    def getNode(self,index):
        i = 1
        node = self.head_node.next

        while index != i and node != self.last_node:
            i += 1
            node = node.next

        return node

def cpuScheduling(Ready_Queue):
    global Tr, Normalize

    time = 0
    Tr = 0
    Normalize = 0

    Queue1 = List(1)
    Queue2 = List(2)
    Queue3 = List(4)
    Queue4 = List(8)

    index = Ready_Queue.getListLen()



    print("--------------------------------------------------")
    print("id\tarr\tser\tfin\ttat\tnor_tat\t")
    print("--------------------------------------------------")

    while 1:
        if Ready_Queue.getListLen() > 0 :
            node = Ready_Queue.getNode(1)
            if node.turn_around_time == time:
                node.arrival = time
                node.queue_time = Queue1.queue_time
                Ready_Queue.delete_node(node)
                Queue1.insert_node(node)

        if Queue1.getListLen() > 0:
            node = Queue1.getNode(1)
            if Queue1.queue_time >= node.queue_time :
                Queue1.burst()
                time += 1
                if node.queue_time == 0 and node.current_computing_time != 0:
                    Queue1.delete_node(node)
                    node.queue_time = Queue2.queue_time
                    Queue2.insert_node(node)

                elif node.current_computing_time == 0 :
                    node.finish = time
                    Queue1.print_node(node)
                    Queue1.delete_node(node)
                continue

        elif Queue2.getListLen() > 0:
            node = Queue2.getNode(1)
            if Queue2.queue_time >= node.queue_time:
                Queue2.burst()
                time += 1
                if node.queue_time == 0 and node.current_computing_time != 0:
                    Queue2.delete_node(node)
                    node.queue_time = Queue3.queue_time
                    Queue3.insert_node(node)

                elif node.current_computing_time == 0:
                    node.finish = time
                    Queue2.print_node(node)
                    Queue2.delete_node(node)
                continue

        elif Queue3.getListLen() > 0:
            node = Queue3.getNode(1)
            if Queue3.queue_time >= node.queue_time:
                Queue3.burst()
                time += 1
                if node.queue_time == 0 and node.current_computing_time != 0:
                    Queue3.delete_node(node)
                    node.queue_time = Queue4.queue_time
                    Queue4.insert_node(node)

                elif node.current_computing_time == 0:
                    node.finish = time
                    Queue3.print_node(node)
                    Queue3.delete_node(node)
                continue

        elif Queue4.getListLen() > 0:
            node = Queue4.getNode(1)
            if Queue4.queue_time >= node.queue_time:
                Queue4.burst()
                time += 1
#                if node.queue_time == 0 and node.current_computing_time != 0:
#                    Queue4.delete_node(node)
#                    Queue2.insert_node(node)

                if node.current_computing_time == 0:
                    node.finish = time
                    Queue4.print_node(node)
                    Queue4.delete_node(node)
                continue

        else :
            Tr = float(Tr/index)
            Normalize = float(Normalize/index)
            print("--------------------------------------------------")
            print("\naverage_tat : "+'%.2f'%Tr)
            print("average_normalized_tat : "+'%.2f'%Normalize)
            break

def Main():
    Ready_Queue = List(0)

    f = open('input.txt','r')

    while 1:
        str = f.readline()
        if str == '':
            break
        num = str.split(',')
        i = 0
        while i < num.__len__():
            i+=1
            if i > 2 :
                list = num[2].split('\n')
                newNode = DNode(int(num[0]), int(num[1]), int(list[0]))
                Ready_Queue.insert_node(newNode)
    f.close()

    cpuScheduling(Ready_Queue)
    input('\n\nPress ENTER to exit')




Main()
