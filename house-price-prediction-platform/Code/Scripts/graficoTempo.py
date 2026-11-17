import requests
import plotly.graph_objects as go

usernames = ["notblanky","afonsocord","daniela7lopes2003","TomasMC"]
project_id = 54601261
access_token = "{gitlab_token}"
base_url = "https://gitlab.com/api/v4"

# Dar update Manualmente semanalmente
week = "Week 2 Hours"
updated_after = "2024-02-11T00:00:00.00Z"
updated_before = "2024-02-20T00:00:00.00Z"

def get_time(username):
    headers = { 'Private-Token': access_token }
    url_template = "{base_url}/projects/{project_id}/issues?" \
                   "assignee_username={username}&updated_after={updated_after}&updated_before={updated_before}"
    url = url_template.format(base_url=base_url, project_id=project_id, username=username,
                            updated_after=updated_after, updated_before=updated_before)

    issues = requests.get(url, headers = headers)

    total_seconds = 0
    issues_to_pay = []
    line_template = "id: {id}    closed: {closed_at}  time spent: {time}\ttitle: {title}\turl: {url}"
    print("Issue statistics for {u} from {f} to {t}:\n".format(u=username,f=updated_after, t=updated_before))
    for issue in issues.json():

        time_val = issue['time_stats']['human_total_time_spent']
        #print(issue['time_stats'])
        total_seconds += issue['time_stats']['total_time_spent']
        issues_to_pay.append(str(issue['id']))

        print(issue)
        line = line_template.format(
            id=issue['id'],
            closed_at=issue['closed_at'],
            title=issue['title'],
            time=time_val,
            url=issue['web_url']
        )
        print(line)
    hours = round(float(total_seconds/3600),2)
    print("")
    print("Hours to pay on all issues: %.2f" % hours)
    print(time_val)
    return hours

hours = []
hours_est = [12 for i in range(4)]
pessoas = ["Óscar","Afonso","Daniela","Tomás"]
for u in usernames:
    hours.append(get_time(u))
    print("\n")

fig = go.Figure()

trace = go.Bar(x=pessoas,
               y=hours_est,
               marker=dict(
                   color="red",
                   opacity=0.7,
                   line_color="black",
                   line_width=1),
               name = "Horas estimadas",
               textposition="outside")

trace2 = go.Bar(x=pessoas,
               y=hours,
               marker=dict(
                   color="blue",
                   opacity=0.7,
                   line_color="black",
                   line_width=1),
                name="Horas realizadas",
                textposition="outside")

layout = go.Layout(barmode="group",
                  yaxis_title="Hours",
                  title=week,
                  title_x=0.5,
                  paper_bgcolor="white")

fig = go.Figure(data=[trace,trace2],layout=layout)

fig.show()