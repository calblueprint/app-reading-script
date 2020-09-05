import random
from pprint import pprint

# Helper Functions

def assign_members(general_members, leadership, app_list, general_app_req, leadership_app_req, app_req, seed):
    # Create shuffled grouped member/app arrays
    # format: [('aivant', 30), ('alison', 30), ('micah', 50), ...]
    members = [(member, general_app_req) for member in general_members]
    members += [(member, leadership_app_req) for member in leadership]
    apps = [(app, app_req) for app in app_list]
    
    # Shuffle arrays
    random.seed(seed) if seed else None
    random.shuffle(members)
    random.shuffle(apps)

    # Initialize assignment dictionaries
    member_assignments = {}
    for member in members:
        member_assignments[member[0]] = []

    app_assignments = {}
    for app in apps:
        app_assignments[app[0]] = []

    
    # Loop through members and apps assigning one by one until limit reached
    app_idx, member_idx, assignment_fail_count = 0, 0, 0
    assignment_fail_limit = max(len(members), len(apps)) # Failure limit to prevent infinite loop
    while (apps or members) and assignment_fail_count < assignment_fail_limit:
        app_id, app_req = apps[app_idx]
        member_name, member_req = members[member_idx]

        # If a member is not already assigned to this app, assign them
        if member_name not in app_assignments[app_id]:
            assignment_fail_count = 0
            member_assignments[member_name].append(app_id)
            app_assignments[app_id].append(member_name)
        else: # Else, increase fail count.
            assignment_fail_count += 1

        # Check for completion and increment indices
        if len(app_assignments[app_id]) >= app_req:
            apps.pop(app_idx)
        else:
            app_idx += 1

        if len(member_assignments[member_name]) >= member_req:
            members.pop(member_idx)
        else:
            member_idx += 1
        
        # Avoid mod by 0 error below
        if not members or not apps:
            break

        # Make sure indices haven't exceeded array length
        member_idx = member_idx % len(members)
        app_idx = app_idx % len(apps)
    return member_assignments, app_assignments, assignment_fail_count < assignment_fail_count < assignment_fail_limit

def compute_stats(title, population, assignments):
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
    print("Counts:")
    pprint(counts)

def import_file(filename):
    with open(input_folder + filename) as f:
        return f.read().splitlines()

def export_assignments_together(filename, mem_assignments):
    with open(output_folder + filename, 'w') as f:
        rows = []
        for member, assignments in mem_assignments.items(): 
            assignments_with_links = ['"=HYPERLINK(""{0}"",""{1}"")"'.format(application_link + str(a), a) for a in assignments]
            rows.append(member + ',' + ','.join(assignments_with_links))
        f.write('\n'.join(rows))
    
def export_assignments_separately(mem_assignments):
    for member, assignments in mem_assignments.items():
        with open("{0}{1}.csv".format(output_folder, member.replace(' ', '_')), 'w') as f:
            assignments_with_links = [f"{a},{application_link + str(a)}" for a in assignments]
            f.write('\n'.join(assignments_with_links))

# Constants
output_folder = 'output/'
input_folder = 'input/'
application_link = 'https://calblueprint.org/admins/student_applications/'

# Parameters
seed = 42 # change number to get different assignments, None for random
general_app_req = 25
leadership_app_req = 25
app_req = 5
output_mode = 0 # 0 for single table, 1 for separate tables


# Import files
general_members = import_file('general.txt')
leadership = import_file('leadership.txt')
app_list = import_file('apps.txt')

# Overview
total_apps_to_read_mems = len(general_members) * general_app_req + len(leadership) * leadership_app_req
total_apps_to_read_apps = len(app_list) * app_req
print("OVERVIEW\
    \nThere are {0} general members, {1} leadership members, and {2} applications\
    \nGeneral Members are reading max {3} apps\
    \nLeadership members are reading max {4} apps\
    \nEach app will be read max {5} times\
    \nIf all apps meet requirements, there will be {6} reads\
    \nIf all members meet requirements, there will be {7} reads\n".format(len(general_members), len(leadership), len(app_list), general_app_req, leadership_app_req, app_req, total_apps_to_read_apps, total_apps_to_read_mems))

# Create assignments
print("Assigning Apps...")
mem_assignments, app_assignments, enough_apps = assign_members(general_members, leadership, app_list, general_app_req, leadership_app_req, app_req, seed)
print("Assignment complete!")

# Compute stats
compute_stats("general member assignments", general_members, mem_assignments)
compute_stats("leadership assignments", leadership, mem_assignments)
compute_stats("application assignments", app_list, app_assignments)

if not enough_apps:
    print("NOTE: Not enough apps to complete assignments. Please look at overview and adjust requirements.")
# Export assignments
print("Exporting...")

if output_mode:
    export_assignments_separately(mem_assignments)
else:
    export_assignments_together('output.csv', mem_assignments)