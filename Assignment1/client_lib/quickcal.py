RTT = [0.285823402, 0.286060972, 0.268449750, 0.268433584, 0.265891130, 0.292579217]
Estimated  = RTT[0]
alpha = 1/8
print(f"Estimate 0: {Estimated}")
for x in range(1,6):
    Estimated = Estimated * (1 - alpha) + alpha * RTT[x]
    print(f"Estimate {x}: {round(Estimated, 9)}")