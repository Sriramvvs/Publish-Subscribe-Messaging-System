from xmlrpc.server import SimpleXMLRPCServer

topics = {}  # dictionary to store topics and ports
heartbeat_log = {}  # optional: track heartbeat times

def reg_topic():
    port = 8001 + len(topics)
    topic_name = f"topic_{port}"
    topics[topic_name] = port
    print(f"Registered topic: {topic_name} on port {port}")
    return port

def reg_heartbeat(port):
    print(f"✅ Heartbeat received from broker on port {port}")
    heartbeat_log[port] = "alive"
    return True

server = SimpleXMLRPCServer(("localhost", 8000), logRequests=True)
server.register_function(reg_topic, "reg_topic")
server.register_function(reg_heartbeat, "reg_heartbeat")
print("Topic server running on port 8000...")
server.serve_forever()
