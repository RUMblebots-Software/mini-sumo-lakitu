import rclpy
from rclpy.node import Node
from visualization_msgs.msg import Marker

class HelloRobot(Node):

	def __init__(self):
		super().__init__('hello_robot')
		self.publisher = self.create_publisher(Marker, 'visualization_marker', 10)
		self.timer = self.create_timer(1.0, self.publish_marker)

	def publish_marker(self):
		marker = Marker()
		marker.header.frame_id = "map"
		marker.type = Marker.SPHERE
		marker.action = Marker.ADD
		marker.pose.position.x = 0.0
		marker.pose.position.y = 0.0
		marker.pose.position.z = 0.5
		marker.scale.x = 1.0
		marker.scale.y = 1.0
		marker.scale.z = 1.0
		marker.color.a = 1.0 # Alpha (transparency)
		marker.color.r = 0.0 # Red
		marker.color.g = 1.0 # Green
		marker.color.b = 0.0 # Blue
		self.publisher.publish(marker)
		self.get_logger().info('Publishing green sphere to RViz2!')

def main(args=None):
	rclpy.init(args=args)
	node = HelloRobot()
	rclpy.spin(node)
	rclpy.shutdown()

if __name__ == "__main__":
	main()
