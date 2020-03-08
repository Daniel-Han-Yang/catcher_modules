from typing import Union

from catcher.utils.logger import warning

default_ports = {
    'postgresql': 5432,
    'mysql+pymysql': 3306,
    'mssql+pymssql': 1433,
    'oracle+cx_oracle': 1521
}


def get_engine(conf: Union[str, dict], driver: str = 'postgresql'):
    if not isinstance(conf, str):
        conf_str = '{}://{}:{}@{}:{}/{}'.format(driver,
                                                conf['user'],
                                                conf['password'],
                                                conf['host'],
                                                conf.get('port', default_ports.get(driver.lower(), '')),
                                                conf['dbname'])
    else:
        conf_str = __fill_dialect(conf, driver)
    from sqlalchemy import create_engine
    return create_engine(conf_str)


def __fill_dialect(url: str, driver: str):
    if '://' not in url:  # simple case - user:password@host:port/database
        return driver + '://' + url
    else:
        if '+' in url or url.startswith('postgresql'):
            return url  # dialect specified - mysql+pymysql://user:password@host:port/database
        else:  # no dialect - need to set up dialect from driver
            driver_used = url.split(':')[0]
            found = [k for k in default_ports.keys() if k.startswith(driver_used)]
            if not found:
                warning('Can\'t find dialect for driver ' + driver_used + '. Will try default ' + driver)
                found = [driver]
            return found[0] + ':' + ':'.join(url.split(':')[1:])
