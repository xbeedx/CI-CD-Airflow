import airflow
from datetime import timedelta
from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator

args = {
    'id' : 'practice',
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(2),
    'schedule_interval' : timedelta(days=1),
}

dag = DAG(
    dag_id='practice',
    default_args=args,
    description='A simple tutorial DAG',
    schedule_interval = timedelta(days=1),
)

tasks = []

for i in range(1, 5):
    task = BashOperator(
        task_id=f'task_{i}',
        bash_command='echo {{task_instance_key_str}}',
        dag=dag,
    )
    tasks.append(task)

final_task = BashOperator(
    task_id='final_task',
    bash_command='echo "CIAO :)"',
    dag=dag,
)

tasks[0] >> tasks[1] >> tasks[2] >> tasks[3] >> final_task