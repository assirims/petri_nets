from lib.helper import Helper


# TODO: it doesn't work
class ReversibilityChecker(object):
    def __init__(self, states_list):
        self.states_list = states_list

    def is_network_reversible(self):
        for state in self.states_list:
            states_queue = [state[0]]
            if self.__is_root(state):
                continue

            found_root_state = False
            reached_states = []
            while states_queue:
                state_id = states_queue.pop(0)
                state_obj = Helper.find_state_by_id(self.states_list, state_id)
                if self.__is_root(state_obj):
                    found_root_state = True
                    break

                reached_states.append(state_id)
                print 'Reached state: ', reached_states
                print 'Children: ', self.__find_children(state_obj)
                filtered_state_children = list(set(self.__find_children(state_obj))-set(reached_states)-set(states_queue))
                print 'FilteredStateChildren: ', list(set(self.__find_children(state_obj))-set(reached_states)-set(states_queue))
                states_queue.extend(filtered_state_children)

            print '-------------------------------'
            if not found_root_state:
                return False

        return True

    def __is_root(self, state):
        return state[0] == 0

    def __find_children(self, parent_state):
        children_states_ids = []
        for state in self.states_list:
            if state[1] == parent_state[0]:
                children_states_ids.append(state[0])

        for state_id in parent_state[3]:
            children_states_ids.append(state_id)

        return children_states_ids
