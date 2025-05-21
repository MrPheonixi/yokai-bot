class Queue():
    def __init__(self):
        self.queue = {}
    
    async def add_member(self, id : int, yokai : str):
        #try to see if the member is already in the list
        try :
            self.queue[id].append(yokai)
        except KeyError:
            self.queue[id] = [yokai]
        
    async def show(self, id : int):
        #try to see if the member has a queue (si c'est un homme je pense oui ;-)
        try : 
            qeue = self.queue[id]
        except KeyError:
            qeue = []
        return qeue

    async def delete(self, id : int, yokai : str):
        #try to see if the yokai is in the queue
        try :
            self.queue[id].remove(yokai)
        except:
            return
        
        #delete the user from the queue his is empty
        if self.queue[id] == []:
            self.queue.pop(id)
        