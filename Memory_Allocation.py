from tkinter import *
from tkinter import messagebox
from queue import PriorityQueue

def sortbysec(a, b):
    if a[0][0] == b[0][0]:
        return a[0][1] < b[0][1]
    return a[0][0] > b[0][0]

def run_algorithm():
    holes = []
    holesnextfit = []
    holesbestfit = []
    holesworstfit = PriorityQueue()
    finalfit = []
    try:
        n = int(holes_entry.get())
        for i in range(n):
            a = int(holes_entries[i].get())
            holes.append((a, a))
            holesnextfit.append((a, a))
            holesworstfit.put((a, i + 1))
            holesbestfit.append((a, i + 1))
    except ValueError:
        messagebox.showerror("Error", "Please enter valid integer values for holes")
        return

    try:
        m = int(processes_entry.get())
        process = []
        processnextfit = []
        processworstfit = []
        processbestfit = []
        for i in range(m):
            a = int(processes_entries[i].get())
            process.append((a, i + 1))
            processnextfit.append((a, i + 1))
            processworstfit.append(a)
            processbestfit.append(a)
    except ValueError:
        messagebox.showerror("Error", "Please enter valid integer values for processes")
        return
    
    # First Fit
    firstfit = [[] for _ in range(n)]
    holes_copy = holes.copy()
    completed = []
    c1 = 0
    for i in range(m):
        for j in range(n):
            if process[i][0] <= holes_copy[j][1]:
                holes_copy[j] = (holes_copy[j][0], holes_copy[j][1] - process[i][0])
                firstfit[j].append(i + 1)
                c1 += 1
                break
    completed.append((c1, 1))
    mini_firstfit = min(h[1] for h in holes_copy)
    maxi_firstfit = max(h[1] for h in holes_copy)
    finalfit.append(((maxi_firstfit,mini_firstfit),"First Fit",firstfit))
    # Next Fit
    nextfit = [[] for _ in range(n)]
    holes_copy = holes[:]
    j = 0
    c2 = 0
    for i in range(m):
        cnt = n
        while cnt > 0:
            if processnextfit[i][0] <= holesnextfit[j][1]:
                nextfit[j].append(i + 1)
                holesnextfit[j] = (holesnextfit[j][0], holesnextfit[j][1] - processnextfit[i][0])
                c2 += 1
                break
            else:
                j += 1
                j %= n
            cnt -= 1
    completed.append((c2, 2))
    mini_nextfit = min(h[1] for h in holesnextfit)
    maxi_nextfit = max(h[1] for h in holesnextfit)
    finalfit.append(((maxi_nextfit,mini_nextfit),"Next Fit",nextfit))
    # Best Fit
    bestfit = [[] for _ in range(n)]
    holes_copy = holes[:]
    c3 = 0
    for i in range(m):
        best_hole_index = -1
        best_hole_size = float('inf')
        for j in range(n):
            if processbestfit[i] <= holesbestfit[j][0] and holesbestfit[j][0] < best_hole_size:
                best_hole_index = j
                best_hole_size = holesbestfit[j][0]
        if best_hole_index != -1:
            holesbestfit[best_hole_index] = (holesbestfit[best_hole_index][0] - processbestfit[i], holesbestfit[best_hole_index][1])
            bestfit[best_hole_index].append(i + 1)
            c3 += 1
    completed.append((c3, 3))
    mini_bestfit = min(holesbestfit[j][0] for j in range(n))
    maxi_bestfit = max(holesbestfit[j][0] for j in range(n))
    finalfit.append(((maxi_bestfit, mini_bestfit), "Best Fit", bestfit))

    # Worst Fit
    worstfit = [[] for _ in range(n)]
    holes_copy = holes.copy()
    # holes_copy.sort(reverse=True)
    # holes_copy.reverse()
    c4 = 0
    Size=len(holes_copy)-1
    for i in range(m):
        worst_hole_idx = -1
        worst_hole_size = float('0')
        for j in range(n):
            if(process[i][0]<= holes_copy[j][1] and holes_copy[j][1]>worst_hole_size):
                worst_hole_idx=j
                worst_hole_size=holes_copy[j][1]
        if(worst_hole_idx!=-1):
            holes_copy[worst_hole_idx]=(holes_copy[worst_hole_idx][0],holes_copy[worst_hole_idx][1]-process[i][0])
            worstfit[worst_hole_idx].append(i+1)
            c4+=1
        # holes_copy.sort(reverse=True)
        # holes_copy.reverse()
    completed.append((c4, 4))
    maxi_worstfit = max(h[1] for h in holes_copy)
    mini_worstfit = min(h[1] for h in holes_copy)
    finalfit.append(((maxi_worstfit, mini_worstfit), "Worst Fit", worstfit))

    # Display the best algorithm
    max_completed = max(completed, key=lambda x: x[0])
    best_algorithm = ""
    cnt=0
    AnsList=[]
    for i in completed:
        if(i[0]==max_completed):
            cnt=cnt+1
            AnsList.append((i[0],i[1]))
    if(cnt==1):
        if max_completed[1] == 1:
            best_algorithm = "First Fit"
        elif max_completed[1] == 2:
            best_algorithm = "Next Fit"
        elif max_completed[1] == 3:
            best_algorithm = "Best Fit"
        elif max_completed[1] == 4:
            best_algorithm = "Worst Fit"
        result_label.config(text=f"The best process is {best_algorithm}")
    if(cnt>=2):
        BestMin= float('inf')
        BestMax=0
        BestAlgo=[]
        for i in AnsList:
            BestAlgo.append((finalfit[i[1]-1][0][1],finalfit[i[1]-1][0][0]),finalfit[i[1]-1][1])
        BestAlgo.sort(key=sortbysec)
        for i in BestAlgo:
            print(i)
        print("i over")
        result_label.config(text=f"The best process is {BestAlgo[0][1]}")
    # Display processes allocated to each hole
    processes_allocated_frame = Frame(scrollable_frame)
    processes_allocated_frame.pack()

    for fit in finalfit:
        algorithm_frame = Frame(processes_allocated_frame)
        algorithm_frame.pack()
        alloc_label = Label(algorithm_frame, text=f"{fit[1]} - Allocated Processes:")
        alloc_label.pack(side=LEFT)
        for j, alloc in enumerate(fit[2]):
            hole_info = f"{holes[j][0]} -->> | "
            if not alloc:
                hole_info += " - "
                # hole_info+="\n"
            else:
                for p in alloc:
                    hole_info += f"P{p} | "
                # hole_info+="\n"
            hole_label = Label(algorithm_frame, text=hole_info)
            hole_label.pack(side=LEFT)

    # Scroll to the bottom of the frame
    canvas.configure(scrollregion=canvas.bbox("all"))

# Create GUI
root = Tk()
root.title("Memory Allocation Algorithm")

scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)

canvas = Canvas(root, yscrollcommand=scrollbar.set)
canvas.pack(side=LEFT, fill=BOTH, expand=True)

scrollbar.config(command=canvas.yview)

scrollable_frame = Frame(canvas)
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

Label(scrollable_frame, text="Enter the number of holes:").pack()
holes_entry = Entry(scrollable_frame)
holes_entry.pack()

holes_entries = []
Label(scrollable_frame, text="Enter sizes of each hole:").pack()

def create_holes_entries():
    try:
        n = int(holes_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter valid integer values for holes")
        return

    for i in range(n):
        entry = Entry(scrollable_frame)
        entry.pack()
        holes_entries.append(entry)

Button(scrollable_frame, text="Create Holes Entries", command=create_holes_entries).pack()

Label(scrollable_frame, text="Enter the number of processes:").pack()
processes_entry = Entry(scrollable_frame)
processes_entry.pack()

processes_entries = []
Label(scrollable_frame, text="Enter sizes of each process:").pack()

def create_processes_entries():
    try:
        m = int(processes_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter valid integer values for processes")
        return

    for i in range(m):
        entry = Entry(scrollable_frame)
        entry.pack()
        processes_entries.append(entry)

Button(scrollable_frame, text="Create Processes Entries", command=create_processes_entries).pack()

Button(scrollable_frame, text="Run Algorithm", command=run_algorithm).pack()

holes_label = Label(scrollable_frame, text="")
holes_label.pack()

result_label = Label(scrollable_frame, text="")
result_label.pack()

canvas.configure(scrollregion=canvas.bbox("all"))
canvas.pack(side=LEFT, fill=BOTH, expand=True)
scrollbar.config(command=canvas.yview)

root.mainloop()