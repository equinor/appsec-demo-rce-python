# NOTE: This is a bad example on purpose. Don't take inspiration from this code.

import yaml
import flask 
from reservoir_sim_utils import check_config

app = flask.Flask(__name__, template_folder='/myapp/resources')

@app.route('/', methods=['GET', 'POST'])
def home():

    # On a POST Request
    if flask.request.method == 'POST':

        # Get the YAML code as a string from the form
        yaml_code = flask.request.form.get('yaml')
        try:
            print(yaml_code)
            # Create a dictionary from the YAML string
            yaml_read = yaml.load(yaml_code, Loader=yaml.Loader)
            
            # Check if the configuration is valid
            is_valid = check_config(yaml_read)

            # If not valid, return an error message
            if not is_valid:
                return 'Invalid configuration &#10060;'
            
            # Otherwise return the configuration with a nice indentation
            pretty_yaml = yaml.dump(yaml_read, default_flow_style=False)            
            pretty_yaml = pretty_yaml.replace('\n', '<br/>').replace(' ', '&nbsp;')
            return 'The configuration is valid &#9989;<br/><br/><pre>{}</pre><br/>'.format(pretty_yaml)
        
        except yaml.YAMLError as e:
            # If there is an error parsing the YAML code, return an error message
            return 'Invalid YAML code<br/><br/>Error: <br/>{}'.format(e)
        
        except Exception as e:
            # If there is an error, return an error message
            return 'ERROR:<br/>  {}<br/><br/>INPUT<br/>  {}<br/><br/>YAML<br/>  {}'.format(
                e,
                yaml_code,
                yaml_read if yaml_read is not None else 'None')
    
    return flask.render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=9999)

