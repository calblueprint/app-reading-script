import random
from pprint import pprint

# Helper Functions

def assign_members(members, apps):
    # initialize assignment dictionaries (both ways so it's easy to keep track)
    member_assignments = {}
    app_assignments = {}
    for member in members:
        member_assignments[member[0]] = []

    for app in apps:
        app_assignments[app] = []

    
    # loop through members and apps assigning one by one until all members have hit their requirement
    # note: if there are not enough apps, this will result in an infinite loop :D 
    app_idx = 0
    member_idx = 0
    while members:
        app_id = apps[app_idx]
        member_name, member_req = members[member_idx]

        # If a member is not already assigned to this app, assign them
        if member_name not in app_assignments[app_id]: 
            member_assignments[member_name].append(app_id)
            app_assignments[app_id].append(member_name)
        app_idx += 1

        # If the member has reached their limit, remove them from the pool
        if len(member_assignments[member_name]) >= member_req:
            members.pop(member_idx)
        else:
            member_idx += 1
        
        # If we've run out of members, stop the script
        if len(members) == 0:
            break

        # Make sure indices haven't exceeded array length
        member_idx = member_idx % len(members)
        app_idx = app_idx % len(apps)
    return member_assignments, app_assignments

def compute_stats(title, population, assignments, compute_counts=False):
    print(f"\nComputing stats for {title}")
    sumv, minv, maxv = 0, None, None
    counts = {}
    for member in population:
        num = len(assignments[member])
        sumv += num
        minv = min(num, minv) if minv else num
        maxv = max(num, maxv) if maxv else num
        counts[num] = counts.get(num, 0) + 1
    avgv = sumv/len(population)
    print(f"Avg # assigned: {avgv}\nMin # assigned: {minv}\nMax # assigned: {maxv}")
    if compute_counts:
        print("Counts:")
        pprint(counts)

def import_file(filename):
    with open(input_folder + filename) as f:
        return f.read().splitlines()

def export_assignments(filename, assignments):
    with open(output_folder + filename, 'w') as f:
        assignments_with_links = [f"{a},{application_link + str(a)}" for a in assignments]
        f.write('\n'.join(assignments_with_links))


# Parameters
random.seed(42) # change number to get different assignments
general_app_req = 30
leadership_app_req = 50
output_folder = 'output/'
input_folder = 'input/'
application_link = 'https://calblueprint.org/admins/student_applications/'

# Import files
general_members = import_file('general.txt')
leadership = import_file('leadership.txt')
# apps = import_file('apps.txt')
apps = list(range(1, 301))

# Create member array and shuffle
# format: [('aivant', 30), ('alison', 30), ('micah', 50), ...]
members = [(member, general_app_req) for member in general_members]
members += [(member, leadership_app_req) for member in leadership]
random.shuffle(members)

# Overview
total_apps_to_read = len(general_members) * general_app_req + len(leadership) * leadership_app_req
print("There are {0} applications total\nGeneral Members are reading {1} apps\nLeadership is reading {2} apps\nIn total, {3} apps will be read\n".format(len(apps), general_app_req, leadership_app_req, total_apps_to_read))

# Create assignments
print("Assigning Apps...")
mem_assignments, app_assignments = assign_members(members, apps)
print("Assignment complete!")

# Compute stats
compute_stats("general member assignments", general_members, mem_assignments)
compute_stats("leadership assignments", leadership, mem_assignments)
compute_stats("application assignments", apps, app_assignments, compute_counts=True)

# Export assignments
print("Exporting...")
for member, assignments in mem_assignments.items():
    export_assignments(f"{member.replace(' ', '_')}.txt", assignments)   