# 이중 연결 리스트를 이용한 멀티 피드백 큐 알고리즘

# 노드
class DNode:
    def __init__(self,id,arrival,computing_time,queue_time = None,current_computing_time=None,prev=None, next=None):
        self.id = id    #프로세스 아이디
        self.computing_time = computing_time    #입력된 프로세스 cpu burst time
        self.current_computing_time = computing_time    #현재 남은 cpu burst time
        self.queue_time = None                        #해당 큐에서의 남은 시간
        self.arrival = arrival                      #프로세스가 입력된 시간
        self.finish = None                          #프로세스 종료 시간

        self.prev = prev                                #이전 노드
        self.next = next                                #다음 노드

# 리스트로 큐 구현
class List:
    # 리스트의 헤드 노드, 꼬리 노드 생성, 큐에 시간 할당
    def __init__(self, t):
        self.head_node = DNode(None, None, None, None, None)
        self.last_node = DNode(None, None, None, None, None)

        self.head_node.next = self.last_node
        self.last_node.prev = self.head_node
        self.queue_time = t

    #큐의 첫 번째 노드 cpu burst (크기 1만큼만 cpu burst)
    def burst(self):
        node = self.head_node.next
        node.current_computing_time -= 1
        node.queue_time -= 1

    # 해당 노드 콘솔 출력
    def print_node(self,node):
        global Tr,Normalize
        Tr += float(node.finish - node.arrival)     #프로세스들의 평균 반환시간 계산 과정
        Normalize += float(node.finish - node.arrival)/node.computing_time      #프로세스들의 평균 정규화된 반환시간 계산 과정
        tat = node.finish-node.arrival                  #해당 프로세스의 반환시간 계산
        nor_tat = float(float(node.finish - node.arrival)/node.computing_time)      #해당 프로세스의 정규화된 반환시간 계산
        print(str(node.id) + "\t" + str(node.arrival) + "\t" + str(node.computing_time) +"\t"+str(node.finish)+"\t"+str(tat)+"\t"+'%.2f'%nor_tat)

    # 노드 삽입
    def insert_node(self,new_node):

        new_node.next = self.last_node
        new_node.prev = self.last_node.prev
        self.last_node.prev.next = new_node
        self.last_node.prev = new_node

    # 노드 삭제
    def delete_node(self,del_node):
        if (del_node == self.head_node):
            return
        del_node.prev.next = del_node.next
        del_node.next.prev = del_node.prev

        #del del_node           아직 종료되지 않은 프로세스는 다음 큐에 다시 삽입해야 하므로 객체는 남아있음

    # 리스트의 길이 반환 (해당 큐의 프로세스 갯수 반환)
    def getListLen(self):
        len = 0
        node = self.head_node.next

        while node != self.last_node:
            len += 1
            node = node.next

        return len

    # 인자로 받은 인덱스에 해당하는 노드 반환
    def getNode(self,index):
        i = 1
        node = self.head_node.next

        while index != i and node != self.last_node:
            i += 1
            node = node.next

        return node

# cpu스케줄링 함수
def cpuScheduling(Ready_Queue):
    global Tr, Normalize

    time = 0                #현재 시간
    Tr = 0                  #프로세스들의 평균 반환시간 계산과정
    Normalize = 0           #프로세스들의 평균 정규화된 반환시간 계산과정

    # 총 4개의 큐가 있다. (각각 리스트 객체)
    Queue1 = List(1)        #큐1
    Queue2 = List(2)        #큐2
    Queue3 = List(4)        #큐3
    Queue4 = List(8)        #큐4
    Queue5 = List(16)  # 큐5
    Queue6 = List(32)  # 큐6
    Queue7 = List(64)  # 큐7
    Queue8 = List(128)  # 큐8
    Queue9 = List(256)  # 큐9


    index = Ready_Queue.getListLen()        #입력된 프로세스의 갯수


    # 출력 양식
    print("--------------------------------------------------")
    print("id\tarr\tser\tfin\ttat\tnor_tat\t")
    print("--------------------------------------------------")

    # 모든 프로세스가 종료될 때 까지 반복
    while 1:
        # 준비큐에 있는 프로세스 중 입력 시간이 된 프로세스는 큐1에 삽입 (매 시간마다 확인)
        if Ready_Queue.getListLen() > 0 :
            node = Ready_Queue.getNode(1)
            if node.arrival == time:
                node.arrival = time
                node.queue_time = Queue1.queue_time
                Ready_Queue.delete_node(node)
                Queue1.insert_node(node)

        # 큐 1에 프로세스가 남아있다면 첫 번째 프로세스 cpu burst
        if Queue1.getListLen() > 0:
            node = Queue1.getNode(1)
            if Queue1.queue_time >= node.queue_time :
                Queue1.burst()
                time += 1
                # 큐에 할당된 시간을 다 썼지만 cpu burst time이 남았다면 다음 큐로 떨어짐
                if node.queue_time == 0 and node.current_computing_time != 0:
                    Queue1.delete_node(node)
                    node.queue_time = Queue2.queue_time
                    Queue2.insert_node(node)

                # cpu burst time 이 0이라면 프로세스 종료
                elif node.current_computing_time == 0 :
                    node.finish = time
                    Queue1.print_node(node)
                    Queue1.delete_node(node)
                continue

        # 큐 2에 프로세스가 남아있다면 첫 번째 프로세스 cpu burst
        elif Queue2.getListLen() > 0:
            node = Queue2.getNode(1)
            if Queue2.queue_time >= node.queue_time:
                Queue2.burst()
                time += 1
                # 큐에 할당된 시간을 다 썼지만 cpu burst time이 남았다면 다음 큐로 떨어짐
                if node.queue_time == 0 and node.current_computing_time != 0:
                    Queue2.delete_node(node)
                    node.queue_time = Queue3.queue_time
                    Queue3.insert_node(node)

                # cpu burst time 이 0이라면 프로세스 종료
                elif node.current_computing_time == 0:
                    node.finish = time
                    Queue2.print_node(node)
                    Queue2.delete_node(node)
                continue

        # 큐 3에 프로세스가 남아있다면 첫 번째 프로세스 cpu burst
        elif Queue3.getListLen() > 0:
            node = Queue3.getNode(1)
            if Queue3.queue_time >= node.queue_time:
                Queue3.burst()
                time += 1
                # 큐에 할당된 시간을 다 썼지만 cpu burst time이 남았다면 다음 큐로 떨어짐
                if node.queue_time == 0 and node.current_computing_time != 0:
                    Queue3.delete_node(node)
                    node.queue_time = Queue4.queue_time
                    Queue4.insert_node(node)

                # cpu burst time 이 0이라면 프로세스 종료
                elif node.current_computing_time == 0:
                    node.finish = time
                    Queue3.print_node(node)
                    Queue3.delete_node(node)
                continue

        # 큐 4에 프로세스가 남아있다면 첫 번째 프로세스 cpu burst
        elif Queue4.getListLen() > 0:
            node = Queue4.getNode(1)
            if Queue4.queue_time >= node.queue_time:
                Queue4.burst()
                time += 1
                if node.queue_time == 0 and node.current_computing_time != 0:
                    Queue4.delete_node(node)
                    node.queue_time = Queue5.queue_time
                    Queue5.insert_node(node)

                # cpu burst time 이 0이라면 프로세스 종료
                if node.current_computing_time == 0:
                    node.finish = time
                    Queue4.print_node(node)
                    Queue4.delete_node(node)
                continue

        # 큐 5에 프로세스가 남아있다면 첫 번째 프로세스 cpu burst
        elif Queue5.getListLen() > 0:
            node = Queue5.getNode(1)
            if Queue5.queue_time >= node.queue_time:
                Queue5.burst()
                time += 1
                if node.queue_time == 0 and node.current_computing_time != 0:
                    Queue5.delete_node(node)
                    node.queue_time = Queue6.queue_time
                    Queue6.insert_node(node)

                # cpu burst time 이 0이라면 프로세스 종료
                if node.current_computing_time == 0:
                    node.finish = time
                    Queue5.print_node(node)
                    Queue5.delete_node(node)
                continue

        # 큐 6에 프로세스가 남아있다면 첫 번째 프로세스 cpu burst
        elif Queue6.getListLen() > 0:
            node = Queue6.getNode(1)
            if Queue6.queue_time >= node.queue_time:
                Queue6.burst()
                time += 1
                if node.queue_time == 0 and node.current_computing_time != 0:
                    Queue6.delete_node(node)
                    node.queue_time = Queue7.queue_time
                    Queue7.insert_node(node)

                # cpu burst time 이 0이라면 프로세스 종료
                if node.current_computing_time == 0:
                    node.finish = time
                    Queue6.print_node(node)
                    Queue6.delete_node(node)
                continue

        # 큐 7에 프로세스가 남아있다면 첫 번째 프로세스 cpu burst
        elif Queue7.getListLen() > 0:
            node = Queue7.getNode(1)
            if Queue7.queue_time >= node.queue_time:
                Queue7.burst()
                time += 1
                if node.queue_time == 0 and node.current_computing_time != 0:
                    Queue7.delete_node(node)
                    node.queue_time = Queue8.queue_time
                    Queue8.insert_node(node)

                # cpu burst time 이 0이라면 프로세스 종료
                if node.current_computing_time == 0:
                    node.finish = time
                    Queue7.print_node(node)
                    Queue7.delete_node(node)
                continue

        # 큐 8에 프로세스가 남아있다면 첫 번째 프로세스 cpu burst
        elif Queue8.getListLen() > 0:
            node = Queue8.getNode(1)
            if Queue8.queue_time >= node.queue_time:
                Queue8.burst()
                time += 1
                if node.queue_time == 0 and node.current_computing_time != 0:
                    Queue8.delete_node(node)
                    node.queue_time = Queue9.queue_time
                    Queue9.insert_node(node)

                # cpu burst time 이 0이라면 프로세스 종료
                if node.current_computing_time == 0:
                    node.finish = time
                    Queue8.print_node(node)
                    Queue8.delete_node(node)
                continue

        # 큐 9에 프로세스가 남아있다면 첫 번째 프로세스 cpu burst
        elif Queue9.getListLen() > 0:
            node = Queue9.getNode(1)
            if Queue9.queue_time >= node.queue_time:
                Queue9.burst()
                time += 1
#                if node.queue_time == 0 and node.current_computing_time != 0:
#                    Queue4.delete_node(node)
#                    node.queue_time = Queue5.queue_time
#                    Queue5.insert_node(node)

                # cpu burst time 이 0이라면 프로세스 종료
                if node.current_computing_time == 0:
                    node.finish = time
                    Queue9.print_node(node)
                    Queue9.delete_node(node)
                continue

        # 프로세스가 다 종료되면 평균 반환시간, 평균 정규화된 반환시간 출력후 루프 빠져나감
        else :
            Tr = float(Tr/index)
            Normalize = float(Normalize/index)
            print("--------------------------------------------------")
            print("\naverage_tat : "+'%.2f'%Tr)
            print("average_normalized_tat : "+'%.2f'%Normalize)
            break

def Main():
    # 준비큐 생성
    Ready_Queue = List(0)

    # 읽기 전용으로 파일 오픈
    f = open('input.txt','r')

    # 파일으로 부터 한 줄 씩 읽어와 프로세스 생성 후 준비큐에 삽입
    while 1:
        str = f.readline()
        if str == '':
            break
        num = str.split(',')
        i = 0
        while i < num.__len__():
            i+=1
            if i > 2 :
                # 프로세스의 세 번째 값은 줄바꿈 문자를 포함하기 때문에 split 함수 이용
                list = num[2].split('\n')
                newNode = DNode(int(num[0]), int(num[1]), int(list[0]))
                Ready_Queue.insert_node(newNode)
                
    # 파일 닫기
    f.close()

    # 스케줄링 함수 호출. 인자로 준비큐를 넘겨준다
    cpuScheduling(Ready_Queue)
    
    # exe파일 실행 시 자동 종료 방지
    input('\n\nPress ENTER to exit!!!')




Main()
