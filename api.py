import os
from collections import OrderedDict
from flask import Flask, render_template
from hurry.filesize import size
import psutil


app = Flask(__name__)


@app.route('/', methods=['GET'])
def show_machine_info():
    """Show information about the server.
    """
    def percent(num):
        '''percentage rounded to one decimal
        '''
        return '{}%'.format(round(num, 1))
    app.logger.info('generating information about the server.')
    data = OrderedDict()
    cpus = os.sysconf(os.sysconf_names['SC_NPROCESSORS_ONLN'])
    data['number_of_CPUs'] = cpus
    data['cpu_usage_total'] = percent(psutil.cpu_percent())
    pid = os.getpid()
    py = psutil.Process(pid)
    data['process_cpu_percent'] = percent(py.cpu_percent())
    data['process_memory_percent'] = percent(py.memory_percent())
    memdict = psutil.virtual_memory()._asdict()
    for k, v in memdict.items():
        if 'percent' in k:
            num = percent(v)
        else:
            num = size(v)
        data['memory_{}'.format(k)] = num
    return render_template('machine_info.html', pages=data)


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
