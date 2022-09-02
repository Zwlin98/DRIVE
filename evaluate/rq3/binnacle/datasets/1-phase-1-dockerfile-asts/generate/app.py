if __name__ == '__main__':
  import os
  import sys
  import json
  import tqdm
  import lzma
  import dockerfile
  import multiprocessing


  def process(item):
    VALID_DIRECTIVES = [
      'FROM',
      'RUN',
      'CMD',
      'LABEL',
      'MAINTAINER',
      'EXPOSE',
      'ENV',
      'ADD',
      'COPY',
      'ENTRYPOINT',
      'VOLUME',
      'USER',
      'WORKDIR',
      'ARG',
      'ONBUILD',
      'STOPSIGNAL',
      'HEALTHCHECK',
      'SHELL'
    ]

    try:
      parsed = item[0]

      dockerfile_ast = {
        'type': 'DOCKER-FILE',
        'children': []
      }

      # Check directives
      for directive in parsed:
        if directive.cmd not in VALID_DIRECTIVES:
          # Not valid dockerfile
          raise Exception('found invalid directive {}'.format(directive.cmd))

        if directive.cmd == 'RUN':
          dockerfile_ast['children'].append({
            'type': 'DOCKER-RUN',
            'children': [{
              'type': 'MAYBE-BASH',
              'value': directive.value[0],
              'children': []
            }]
          })
        elif directive.cmd == 'FROM':
          from_node = {
            'type': 'DOCKER-FROM',
            'children': []
          }

          value = directive.value[0]
          name = value.split('/')[-1].strip() if '/' in value else value
          name = name.split(':')[0].strip() if ':' in name else name 

          from_node['children'].append({
            'type': 'DOCKER-IMAGE-NAME',
            'value': name,
            'children': []
          })

          if '/' in value:
            from_node['children'].append({
              'type': 'DOCKER-IMAGE-REPO',
              'value': value.split('/')[0].strip(),
              'children': []
            })
            
          if ':' in value:        
            from_node['children'].append({
              'type': 'DOCKER-IMAGE-TAG',
              'value': value.split(':')[-1].strip() if ':' in value else None,
              'children': []
            })
        
          dockerfile_ast['children'].append(from_node)
        elif directive.cmd == 'COPY':
          copy_node = {
            'type': 'DOCKER-COPY',
            'children': []
          }

          copy_node['children'].append({
            'type': 'DOCKER-COPY-TARGET',
            'children': [{
              'type': 'DOCKER-PATH',
              'value': directive.value[-1],
              'children': []
            }]
          })

          for arg in directive.value[:-1]:
            copy_node['children'].append({
              'type': 'DOCKER-COPY-SOURCE',
              'children': [{
                'type': 'DOCKER-PATH',
                'value': arg,
                'children': []
              }]
            })
          
          dockerfile_ast['children'].append(copy_node)
        elif directive.cmd == 'ADD':
          add_node = {
            'type': 'DOCKER-ADD',
            'children': []
          }

          add_node['children'].append({
            'type': 'DOCKER-ADD-TARGET',
            'children': [{
              'type': 'DOCKER-PATH',
              'value': directive.value[-1],
              'children': []
            }]
          })

          for arg in directive.value[:-1]:
            add_node['children'].append({
              'type': 'DOCKER-ADD-SOURCE',
              'children': [{
                'type': 'DOCKER-PATH',
                'value': arg,
                'children': []
              }]
            })
          
          dockerfile_ast['children'].append(add_node)
        elif directive.cmd == 'EXPOSE':
          dockerfile_ast['children'].append({
            'type': 'DOCKER-EXPOSE',
            'children': [{
              'type': 'DOCKER-PORT',
              'value': directive.value[0],
              'children': []
            }]
          })
        elif directive.cmd == 'WORKDIR':
          dockerfile_ast['children'].append({
            'type': 'DOCKER-WORKDIR',
            'children': [{
              'type': 'DOCKER-PATH',
              'value': directive.value[0],
              'children': []
            }]
          })
        elif directive.cmd == 'VOLUME':
          for arg in directive.value:
            dockerfile_ast['children'].append({
              'type': 'DOCKER-VOLUME',
              'children': [{
                'type': 'DOCKER-PATH',
                'value': arg,
                'children': []
              }]
            })
        elif directive.cmd == 'ARG':
          arg_node = {
            'type': 'DOCKER-ARG',
            'children': [{
              'type': 'DOCKER-NAME',
              'value': directive.value[0] if '=' not in directive.value[0] else directive.value[0].split('=')[0].strip(),
              'children': []
            }]
          }

          if '=' in directive.value[0]:
            arg_node['children'].append({
              'type': 'DOCKER-LITERAL',
              'value': directive.value[0].split('=')[-1].strip(),
              'children': []
            })

          dockerfile_ast['children'].append(arg_node)
        elif directive.cmd == 'ENV':
          for name, value in zip(directive.value[::2], directive.value[1::2]):
            dockerfile_ast['children'].append({
              'type': 'DOCKER-ENV',
              'children': [{
                'type': 'DOCKER-NAME',
                'value': name,
                'children': []
              }, {
                'type': 'DOCKER-LITERAL',
                'value': value,
                'children': []
              }]
            })
        elif directive.cmd == 'entrypoint':
          first = directive.value[0]

          entrypoint_node = {
            'type': 'DOCKER-ENTRYPOINT',
            'children': [{
              'type': 'DOCKER-ENTRYPOINT-EXECUTABLE',
              'value': first,
              'children': []
            }]
          }

          for value in directive.value[1:]:
            entrypoint_node['children'].append({
              'type': 'DOCKER-ENTRYPOINT-ARG',
              'value': value,
              'children': []
            })

          dockerfile_ast['children'].append(entrypoint_node)
        elif directive.cmd == 'CMD':
          cmd_node = {
            'type': 'DOCKER-CMD',
            'children': []
          }

          for value in directive.value:
            cmd_node['children'].append({
              'type': 'DOCKER-CMD-ARG',
              'value': value,
              'children': []
            })

          dockerfile_ast['children'].append(cmd_node)
        elif directive.cmd == 'SHELL':
          first = directive.value[0]

          shell_node = {
            'type': 'DOCKER-SHELL',
            'children': [{
              'type': 'DOCKER-SHELL-EXECUTABLE',
              'value': first,
              'children': []
            }]
          }

          for value in directive.value[1:]:
            shell_node['children'].append({
              'type': 'DOCKER-SHELL-ARG',
              'value': value,
              'children': []
            })

          dockerfile_ast['children'].append(shell_node)
        elif directive.cmd == 'USER':
          dockerfile_ast['children'].append({
            'type': 'DOCKER-USER',
            'children': [{
              'type': 'DOCKER-LITERAL',
              'value': directive.value[0],
              'children': []
            }]
          })
          
      dockerfile_ast['file_sha'] = item[1].split('/')[-1].replace(
        '.Dockerfile', ''
      ).strip()

      return json.dumps(dockerfile_ast)

    except Exception as ex:
      return None


  pool = multiprocessing.Pool()

  all_lines = []
  for line in sys.stdin:
    with open(line.strip()) as dfh:
      try:
        all_lines.append((
          dockerfile.parse_string(dfh.read()),
          line.strip()
        ))
      except Exception:
        continue
    
  results = pool.imap(process, all_lines, chunksize=500)

  with lzma.open('/mnt/outputs/{}.jsonl.xz'.format(sys.argv[1]), mode='wt') as out_file:
    for result in tqdm.tqdm(results, total=len(all_lines), desc="Generating"):
      if result is None:
        continue
      out_file.write('{}\n'.format(result))
