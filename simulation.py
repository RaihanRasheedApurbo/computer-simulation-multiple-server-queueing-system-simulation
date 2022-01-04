import logging
import random
import math

# setting up seed for reproudicible output... helpful for debugging
random.seed(0)

def uniform_random_int(left,right):
    return round(random.uniform(left,right))

def expexponential_random_variable(mean):
    uniform_random_vairable = random.uniform(0, 1)
    ln_uniform_random_variable = math.log(uniform_random_vairable)
    return_value = -1 * mean * ln_uniform_random_variable
    return return_value

def no_elevator_is_available():
    logger.info('hi')

def send_off_tagged_elevator():
    print("hi")

def sumArr(arr,start,finish):
    sum = 0
    for i in range(start,finish+1):
        sum += arr[i]
    return sum

def getMaxIndex(arr):
    highest_index = -1
    for i in range(len(arr)):
        if arr[i] > 0:
            highest_index = i
    if highest_index == -1:
        raise "getMaxIndex error"
    return highest_index

if __name__ == '__main__':

    # logger initialization
    formatter = logging.Formatter(
        "\n*********Line no:%(lineno)d*********\n%(message)s\n***************************"
    )
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger = logging.getLogger("status")
    logger.setLevel(logging.INFO)
    logger.addHandler(stream_handler)




    # input file opening
    input_file = open("input.txt", "rt")  # r-> read t-> text mode

    # store all input in this dictionary
    inputs = {}

    # first line total simulation time
    input_line = input_file.readline()
    inputs["simulation_time"] = int(input_line)

    # second line number of floors, elevators, capacity, batch size 
    input_line = input_file.readline()
    numbers = input_line.split()
    inputs["total_floors"] = int(numbers[0])
    inputs["total_elevators"] = int(numbers[1])
    inputs["total_capacity"] = int(numbers[2])
    inputs["batch_size"] = int(numbers[3])

    # third line door holding time, inter-floor traveling time, opening time, closing time
    input_line = input_file.readline()
    numbers = input_line.split()
    inputs["door_holding_time"] = int(numbers[0])
    inputs["inter_floor_traveling_time"] = int(numbers[1])
    inputs["opening_time"] = int(numbers[2])
    inputs["closing_time"] = int(numbers[3])

    # fourth line passenger embarking and disembarking time
    input_line = input_file.readline()
    numbers = input_line.split()
    inputs["passenger_embarking_time"] = int(numbers[0])
    inputs["passenger_disembarking_time"] = int(numbers[1])

    # fifth line mean interarrival time
    input_line = input_file.readline()
    inputs["mean_interarrival_time"] = float(input_line) * 60

    # input file closing
    input_file.close()

    logger.info(inputs)

    # step 1 initialization of variables
    state = {}
    state["DELTIME"] = 0
    state["ELEVTIME"] = 0
    state["MAXDEL"] = 0
    state["MAXELEV"] = 0
    state["QUELEN"] = 0
    state["QUETIME"] = 0
    state["MAXQUE"] = 0
    state["quetotal"] = 0
    state["remain"] = 0

    # step 2
    i = 1
    # initializing between arr with 1 indexing so first item can be anything
    between = [-1]
    between.append(expexponential_random_variable(inputs["mean_interarrival_time"]))
     # initializing floor arr with 1 indexing so first item can be anything
    floor = [-1]
    floor.append(uniform_random_int(2,inputs["total_floors"]))
    # initializing delivery arr with 1 indexing so first item can be anything
    delivery = [-1]
    delivery.append(inputs["door_holding_time"]) # delivery[1] = 15

    # step 3
    # initialize clock time
    time = between[i]
    # creating return array for all elevators one extra for 1 indexing
    return_time = [-1] * (inputs["total_elevators"] + 1)
    for lift_no in range(inputs["total_elevators"]):
        return_time[lift_no+1] = time        # (lift_no+1) for one indexing
    # making upperbound of customers
    upper_bound_of_customers = math.floor(inputs["simulation_time"]/inputs["mean_interarrival_time"]) * inputs["batch_size"] 
    # assigning wait time to 0 for all customers
    wait = [0] * (upper_bound_of_customers + 1)
    logger.info(upper_bound_of_customers)
    logger.info(return_time)

    # dictionary and array initialization for several states
    # from step 6
    first = {}
    occup = {}
    selvec = {}
    flrvec = {}
    # from step 12
    elevator = {}
    # from step 17
    stop = [0] * (inputs["total_elevators"]+1)
    eldel = [0] * (inputs["total_elevators"]+1)
    operate = [0] * (inputs["total_elevators"]+1)
    # from step 19
    arrive = {}
    # for step 30 to 8
    goto_step_8_flag = False
    # step 4
    while time<=inputs["simulation_time"]:
        # step 5
        
        if not goto_step_8_flag:
            j = -1 # initializing lift no with -1
            for lift_no in range(inputs["total_elevators"]):
                if time >= return_time[lift_no+1]:    # (i+1) for one indexing
                    j = lift_no+1
                    break
            
            if j == -1:
                # no_elevator_is_available() # GOTO step 19
                # step 19
                quecust = i
                startque = time
                queue = 1
                arrive[i] = time
                # step 20
                j = -1 # initializing lift no with -1
                while(True): # used for goto 20
                    i += 1
                    between.append(expexponential_random_variable(inputs["mean_interarrival_time"]))
                    floor.append(uniform_random_int(2,inputs["total_floors"]))
                    time += between[i]
                    arrive[i] = time
                    queue += 1
                    # step 21
                    for lift_no in range(inputs["total_elevators"]):
                        if time >= return_time[lift_no+1]:    # (i+1) for one indexing
                            j = lift_no+1
                            break
                    if j == -1:
                        continue # GOTO step 20
                    else:
                    
                        # step 22
                        selvec[j] = [-1] * (inputs["total_floors"]+1)
                        flrvec[j] = [-1] * (inputs["total_floors"]+1)
                        for k in range(inputs["total_floors"]):
                            selvec[j][k+1] = 0      # k+1 varies from 1 to total_elevators number inclusive
                            flrvec[j][k+1] = 0
                        state["remain"] = queue - inputs["total_capacity"]

                        # step 23
                        if state["remain"] <= 0:
                            R = i
                            occup[j] = queue
                        else:
                            R = quecust + inputs["total_capacity"] - 1
                            occup[j] = inputs["total_capacity"]
                        
                        # step 24
                        for k in range(quecust,R+1):
                            selvec[j][floor[k]] = 1
                            flrvec[j][floor[k]] += 1
                        
                        # step 25
                        if queue >= state["QUELEN"]:
                            state["QUELEN"] = queue
                        
                        # step 26
                        state["quetotal"] += occup[j]
                        state["QUETIME"] += (R-quecust+1) * time - sumArr(quecust,R,arrive)

                        # step 27
                        if(time - startque) >= state["MAXQUE"]:
                            state["MAXQUE"] = time - startque
                        
                        # step 28
                        first[j] = quecust

                        # step 29
                        for k in range(first[j],R+1):
                            delivery[k] = inputs["door_holding_time"] + (time-arrive[k])
                            wait[k] = time - arrive[k]
                        
                        # step 30
                        if state["remain"] <= 0:
                            queue = 0
                            goto_step_8_flag = True
                            break
                            # GOTO step 8 to get next customer
                        else:
                            # do step 12-17 with loop and then goto 31
                            limit = R
                            for k in range(first[j],limit+1):
                                n = floor[k] - 1 # an index   # step 12
                                elevator[k] = 10 * n + 3 * sumArr(flrvec[j],1,n)
                                + 3 + 10 * sumArr(selvec[j],1,n) + 5
                                delivery[k] += elevator[k] # step 13
                                state["DELTIME"] += delivery[k] # step 14
                                if delivery[k] > state["MAXDEL"]: # step 15
                                    state["MAXDEL"] = delivery[k]
                                if elevator[k] > state["MAXELEV"]:
                                    state["MAXELEV"] = elevator[k]

                            # step 17
                            stop[j] += sumArr(selvec[j],1,inputs["total_floors"])
                            max_index = getMaxIndex(selvec[j])
                            eldel[j] = 20*(max_index-1) + 3 * sumArr(flrvec[j],1,inputs["total_floors"])
                            + 10 * sumArr(selvec[j],1,inputs["total_floors"])
                            return_time = time + eldel[j]
                            operate[j] += eldel[j]

                            #  done Steps 12–17.  GOTO Step 31
                            # step 31
                            queue = state["remain"]
                            quecust = R + 1
                            startque = arrive[R+1]
                            
                            
                            # step 32
                            # GOTO step 20 we have go back to while loop of step 4
                            continue
            

        
            logger.info(i)
            logger.info(j)
            # step 6
            
            first[j] = i
            occup[j] = 0
            selvec[j] = [-1] * (inputs["total_floors"]+1)
            flrvec[j] = [-1] * (inputs["total_floors"]+1)
            logger.info(selvec)
            logger.info(flrvec)
            for k in range(inputs["total_floors"]):
                selvec[j][k+1] = 0      # k+1 varies from 1 to total_elevators number inclusive
                flrvec[j][k+1] = 0
            
            logger.info(selvec)
            logger.info(flrvec)
            logger.info(floor[i])
        
        # step 7
        while(True):
            if not goto_step_8_flag:
                selvec[j][floor[i]] = 1
                flrvec[j][floor[i]] += 1
                occup[j] += 1

                logger.info(selvec)
                logger.info(flrvec)
                logger.info(occup)

            goto_step_8_flag = False

            # step 8
            i += 1
            between.append(expexponential_random_variable(inputs["mean_interarrival_time"]))
            floor.append(uniform_random_int(2,inputs["total_floors"]))
            time += between[i]
            delivery.append(inputs["door_holding_time"])
            logger.info(between)
            logger.info(floor)
            logger.info(delivery)

            # step 9
            logger.info(return_time)
            for k in range(inputs["total_elevators"]):
                if time >= return_time[k+1]:
                    return_time[k+1] = time
            logger.info(return_time)

            # step 10
            if between[i] <= inputs["door_holding_time"] and occup[j] < inputs["total_capacity"]:
                for k in range(first[j],i): # k = firstj to i-1  
                    delivery[k] += between[i]
                logger.info(delivery)
                continue
            else:
                break

        # send_off_tagged_elevator() # step 11-18
        limit = i-1
        
        logger.info(limit)
        logger.info(first[j])
        for k in range(first[j],limit+1): # k = firstj to limit # step 11
            n = floor[k] - 1 # an index   # step 12
            elevator[k] = inputs["inter_floor_traveling_time"] * n + inputs["passenger_disembarking_time"] * sumArr(flrvec[j],1,n) + inputs["passenger_disembarking_time"] + (inputs["opening_time"]+inputs["closing_time"]) * sumArr(selvec[j],1,n) + inputs["opening_time"]
            delivery[k] += elevator[k] # step 13
            
            logger.info(elevator[k])
            logger.info(delivery[k])
            logger.info(state["DELTIME"])
            logger.info(state["MAXDEL"])
            logger.info(state["MAXELEV"])

            state["DELTIME"] += delivery[k] # step 14
            if delivery[k] > state["MAXDEL"]: # step 15
                state["MAXDEL"] = delivery[k]
            if elevator[k] > state["MAXELEV"]:
                state["MAXELEV"] = elevator[k]

        # step 17
        stop[j] += sumArr(selvec[j],1,inputs["total_floors"])
        max_index = getMaxIndex(selvec[j])
        eldel[j] = 20*(max_index-1) + 3 * sumArr(flrvec[j],1,inputs["total_floors"])
        + 10 * sumArr(selvec[j],1,inputs["total_floors"])
        return_time = time + eldel[j]
        operate[j] += eldel[j]

            # goto 5 will be done automatically after finishing 18

                
            
        






        # break # this break is not part of the algo and used for finishing the loop

        

    
    






