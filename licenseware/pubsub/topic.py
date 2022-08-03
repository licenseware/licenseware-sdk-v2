from typing import List, Union
from confluent_kafka.admin import AdminClient, NewTopic
from .types import TopicType



class Topic:

    def __init__(self, admin: AdminClient, num_partitions: int = 0, replication_factor: int = 0):
        self.admin = admin
        self.replication_factor = replication_factor
        self.num_partitions = num_partitions


    def new(self, topic: TopicType, num_partitions: int = None, replication_factor: int = None):
        
        assert isinstance(topic, TopicType)

        new_topic = NewTopic(
            topic, 
            num_partitions = num_partitions or self.num_partitions, 
            replication_factor= replication_factor or self.replication_factor
        )

        self._create_topic(new_topic)

        return self


    def _create_topic(self, topic: NewTopic):

        fs = self.admin.create_topics([topic])

        # Wait for each operation to finish.
        for item, f in fs.items():
            try:
                f.result()  # The result itself is None
                print("topic {} created".format(item))
            except Exception as e:
                print("Failed to create topic {}: {}".format(item, e))


    def delete(self, topics:Union[str, List[str]]):

        if isinstance(topics, str):
            topics = [topics]
            
        self.admin.delete_topics(topics)
        

