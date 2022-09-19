import jenkins
from environs import Env

env = Env()
env.read_env()

if __name__ == '__main__':

    server = jenkins.Jenkins(env.str('JENKINS_URL'),
                             username=env.str('LDAP_USERNAME'),
                             password=env.str('LDAP_PASSWORD'))

    for job in server.get_all_jobs():
        if job.get('url') == f"{env.str('JENKINS_URL')}{env.str('JENKINS_FOLDER_URL')}":
            for j in job.get('jobs'):
                copy_job = server.get_job_config(j.get('fullname'))
                try:
                    server.create_job(f"{env.str('FOLDER_TO')}/{env.str('FOLDER_NAME')}/{j.get('name')}",
                                      copy_job.replace(f"{env.str('FOLDER_FROM')}/",
                                                       f"{env.str('FOLDER_TO')}/"))
                    print(f"{j.get('fullname')} is copied")
                except Exception as err:
                    print(err)
