import psycopg2
import boto3
import time
import datetime

# EXAMPLES:
# Parameter Passing 
# cur.execute(
# ...     """INSERT INTO some_table (an_int, a_date, a_string)
# ...         VALUES (%s, %s, %s);""",
# ...     (10, datetime.date(2005, 11, 18), "O'Reilly"))

# >>> cur.execute(
# ...     """INSERT INTO some_table (an_int, a_date, another_date, a_string)
# ...         VALUES (%(int)s, %(date)s, %(date)s, %(str)s);""",
# ...     {'int': 10, 'str': "O'Reilly", 'date': datetime.date(2005, 11, 18)})
class DB():


	"""function obj=observations_db(cfg)
            obj.cfg=cfg;
            obj.colnames.app_tag_colnames.insertion={'label_id','frame','stream'};
            obj.colnames.app_label_colnames.insertion={'title','time_added','time_updated','current_version'};
            obj.colnames.app_class_mapping_colnames.insertion={'class_id','class_name'};
            obj.colnames.app_region_colnames.insertion={'frame','x1','x2','y1','y2','label_version','label_id','scene_id','confidence'};
            obj.colnames.app_scene_colnames.insertion={'path','timestamp','frames','frame_rate','width','height','time_taken','time_added','thumbnail'};
            obj.tablenames.tag_table_name='app_tag';
            obj.tablenames.label_table_name='app_label';
            obj.tablenames.region_table_name='app_region';
            obj.tablenames.scene_table_name='app_scene';
            obj.tablenames.user_selection_table_name='app_user_selection';
            
            obj.tablenames.coreset_table_name = 'app_coreset';
            obj.colnames.app_coreset_colnames.insertion={'scene_id', 'coreset_tree_path', 'coreset_results_path', 'simple_coreset_path'};
            
            %added for test
            obj.tablenames.test_table_name = 'app_test';
            obj.colnames.app_test_colnames.insertion={'text_col', 'int_col', 'float_col', 'time_col', 'next_text_col'};
            
            %synthetic_data_table
            obj.tablenames.synthetic_region_table_name = 'app_synthetic_region';
            obj.colnames.app_synthetic_region_colnames.insertion={'frame','x1', 'x2', 'y1', 'y2', 'class_id', 'confidence', 'importance', 'scene_id'};
        end"""
	def __init__(self):
		#TODO: How to connect to RDS
		self.conn = psycopg2.connect("dbname=postgres user=postgres password=ryansuperurop host=superurop.ceungrwwr3co.us-east-1.rds.amazonaws.com")
		self.cur = self.conn.cursor()
		self.colnames = {'app_tag_colnames':['label_id','frame','stream'],
						'app_labal_colnames':['title','time_added','time_updated','current_version'],
						'app_class_mapping_colnames':['class_id','class_name'],
						'app_region_colnames':['frame','x1','x2','y1','y2','label_version','label_id','scene_id','confidence'],
						'app_scene_colnames':['path','timestamp','frames','frame_rate','width','height','time_taken','time_added','thumbnail'],
						'app_coreset_colnames':['scene_id', 'coreset_tree_path', 'coreset_results_path', 'simple_coreset_path']}
		self.tablenames = {'tag_table_name':'app_tag',
							'label_table_name':'app_label',
							'region_table_name':'app_region',
							'scene_table_name':'app_scene',
							'user_selection_table_name':'app_user_selection',
							'coreset_table_name':'app_coreset'}
		pass

	"""function add_scene(obj,scene)
            table_name='app_scene';
            colnames=obj.colnames.app_scene_colnames.insertion;
            t=format_time_str(obj,now);
            time_taken=t;
            time_added=t;
            label_version=obj.db_version;
            thumbnail=' ';
            data={scene.path,scene.timestamp,scene.frames,scene.frame_rate,scene.width,scene.height,time_taken,time_added,thumbnail};
            datainsert(obj.conn,table_name,colnames,data);
        end"""

	def add_scene(self,scene):
		statement = self.insert_statement(self.tablenames['scene_table_name'],self.colnames['app_scene_colnames'])
		ts = time.time()
		time1 = datetime.datetime.fromtimestamp(ts).strftime('%d-%b-%Y %H:%M:%S')
		time2 = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
		thumbnail = ' '
		data=[scene[0][0],time1,int(scene[1][0][0]),int(scene[2][0][0]),int(scene[3][0][0]),int(scene[4][0][0]),time2,time2,thumbnail];
		#self.cur.execute("SELECT setval('app_scene_id_seq', (SELECT MAX(id) FROM app_scene)+1)")
		self.cur.execute(statement,data)
		self.conn.commit()
		return (scene[0][0],time1)

	"""function add_coreset(obj, scene_label, coreset)
            %first find scene_id
            scene_path = scene_label(1);
            scene_timestamp = scene_label(2);
            scene_query = ['select id from ',obj.tablenames.scene_table_name,' where path = ''',char(scene_path),''' and timestamp=''',char(scene_timestamp),''''];
            cur2=exec(obj.conn,scene_query);
            cur2=fetch(cur2,1);
            scene_id=cur2.Data{1};
            
            table_name = 'app_coreset';
            col_names = obj.colnames.app_coreset_colnames.insertion;
            data = {scene_id, coreset.coreset_tree_path, coreset.coreset_results_path, coreset.simple_coreset_path};
            datainsert(obj.conn, table_name, col_names, data)
        end"""

	def add_coreset(self, scene_label, coreset):
		scene_path = scene_label[0]
		scene_timestamp = scene_label[1]
		scene_query = 'select id from ' +self.tablenames['scene_table_name'] +' where path =%s and timestamp=%s;'
		self.cur.execute(scene_query,scene_label)
		scene_id = self.cur.fetchone()[0]
		statement = self.insert_statement(self.tablenames['coreset_table_name'],self.colnames['app_coreset_colnames'])
		data = [scene_id,coreset['tree'],coreset['results'], coreset['simple']]
		self.cur.execute(statement,data)
		self.conn.commit()

	"""function add_detections_from_frame(obj,detections,scene_label,frame)
            table_name='app_region';
            scene_path = scene_label(1);
            scene_timestamp = scene_label(2);
            % get label names
            scene_query = ['select id from ',obj.tablenames.scene_table_name,' where path = ''',char(scene_path),''' and timestamp=''',char(scene_timestamp),''''];
            cur2=exec(obj.conn,scene_query);
            cur2=fetch(cur2,1);
            scene_id=cur2.Data{1};
            for i = 1:size(detections,1)
                colnames=obj.colnames.app_region_colnames.insertion;
                detection_label=num2str(round(detections(i,1)));
                cur=exec(obj.conn,['select id from ',obj.tablenames.label_table_name,' where title = ''',detection_label,'''']);
                cur=fetch(cur,1);
                label_id=cur.Data{1};
                label_version=obj.db_version;
                detection=struct('x1',detections(i,2),...
                    'y1',detections(i,3),...
                    'x2',detections(i,4),...
                    'y2',detections(i,5),...
                    'frame',frame,...
                    'confidence',detections(i,6));
                data={detection.frame,detection.x1,detection.x2,detection.y1,detection.y2,label_version,label_id,scene_id,detection.confidence};
                datainsert(obj.conn,table_name,colnames,data);
            end
        end"""


	def add_detections_from_frame(self,scores,boxes,scene_label,frame):
		classes_dict = {1:2,2:24,3:26,4:1,5:1,6:33,7:37,8:1,9:43,10:1,11:1,12:58,13:92,14:114,15:124,16:1,17:155,18:164,19:185,20:189}
		label_inc = 4531
		scene_path = scene_label[0]
		scene_timestamp = scene_label[1]
		scene_query = 'select id from ' +self.tablenames['scene_table_name'] +' where path = ' + scene_path + ' and timestamp= '+scene_timestamp + ';'
		self.cur.execute(scene_query)
		scene_id = cur.fetchone()[0]
		for region in range(len(scores)):
			#detection_label = detections[i][0]
			#label_query = 'select id from ' +self.tablenames['label_table_name'] +' where title = ' + detection_label +';'
			#self.cur.execute(label_query)
			#label_id = cur.fetchone()[0]
			for obj in range(1,len(scores[region])):
				label_version = 1
				label_id = classes_dict[i]+label_inc
				obj_ind = obj*4
				x1 = boxes[region][obj_ind]
				y1 = boxes[region][obj_ind+1]
				x2 = boxes[region][obj_ind+2]
				y2 = boxes[region][obj_ind+3]
				confidence  = scores[region][obj]
				data = [frame,x1,x2,y1,y2,label_version,label_id,scene_id,confidence]
				statement = self.insert_statement(self.tablenames['region_table_name'],self.colnames['app_region_colnames'])

	def insert_statement(self,tablename,colnames):
		print tablename
		print ', '.join(colnames)
		return 'INSERT INTO ' + tablename + '(' + ', '.join(colnames) + ') VALUES (' + ','.join(['%s' for i in range(len(colnames))])+');'

	def close(self):
		self.cur.close()
		self.conn.close()
