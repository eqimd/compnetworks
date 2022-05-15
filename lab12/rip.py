import json

class table_entry:
    def __init__(self, address, next_hop, distance):
        self.address = address
        self.next_hop = next_hop
        self.distance = distance

class router:
    def __init__(self, address, networks):
        self.address = address
        self.dest_table = {}
        for netw in networks:
            self.dest_table[netw] = table_entry(netw, netw, 1)
    
    def update_table(self, address, next_hop, distance):
        if distance != INFINITY:
            if address not in self.dest_table.keys():
                self.dest_table[address] = table_entry(address, next_hop, distance + 1)
                return True
            if self.dest_table[address].distance > distance + 1:
                self.dest_table[address].distance = distance + 1
                self.dest_table[address].next_hop = next_hop
                return True
            
        return False

    def get_dist(self, address):
        if address in self.dest_table:
            return self.dest_table[address].distance
        return INFINITY


INFINITY = 16
ROUTERS = []

def show_table(router):
    print(f'{"[Source IP]":25} {"[Destination IP]":25} {"[Next Hop]":25} {"Metric":25}')
    for addr, netw in router.dest_table.items():
        print(f'{router.address:25} {addr:25} {netw.next_hop:25} {netw.distance}')

def rip():
    step = 0
    changed = True
    while changed:
        step += 1
        changed = False
        for cur in ROUTERS:
            for dest in ROUTERS:
                if cur.address != dest.address:
                    neighs = [rt for rt in cur.dest_table.values() if rt.distance == 1]
                    for next in neighs:
                        if next.distance == 1:
                            changed |= cur.update_table(
                                dest.address,
                                next.address,
                                dest.get_dist(next.address)
                            )
            print(f'Simulation step {step} of router {cur.address}:')
            show_table(cur)
            print()

    for router in ROUTERS:
        print(f'Final state of router {router.address}:')
        show_table(router)
        print()


if __name__ == '__main__':
    netws = json.load(open('netw.json'))
    for addr, netw in netws.items():
        ROUTERS.append(router(addr, netw))

    rip()