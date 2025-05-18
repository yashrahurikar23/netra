Project: Netra

#### Problem
With the failure of recent satellite launch, following points came to our understanding: 
- There needs to be systems that can help scientists find the fault anamolies faster in the post failure scenarios. 
- Eventually such systems should predict such faults before time so that such failures can be avoided.
Who it's for?
Scientist and Engineers.

#### Solution?
Practical solution
Building an AI assistant: By Having an AI system, that is intelligent enough to act as an assistant for scientists and engineers, it can process the data related to the mission and can potentially, define the reasons why some anamolly might happen, this will pace up the research and iteration process.
Post failure research process usually require dealing with large amount of data from the launch, this data can be related to:
1. During flight data
2. Past data from the mission
3. Past data from previous missions

Technical solution
1. RAG (Retrival Augmented Generation) 
With the recent advacements, such type of systems are usually built using RAG technique, in which we can store different knowledge bases in a vector
database and then retrive the relevant information based on the user query later on. 
Simple way to understand this is:
- User adds datasource: PDF, CSV, Image, Text
- Process, embedded and store the datasource in vector DB and standard SQL DB if required. This embedding is done using a 
- User sends a query to the system, system embeds and understands the query, matches the best result

2. Fine tuning an existing model with curated dataset for context based processing
3. Reasoning based LLM piepline.



##### Milestones
Milestone 1
1. This will be a standard chat based assistant. The user should be able to add data sources to the system and then 

3. Ability to process data in CSV, JSON, TXT, PDF, Images format. With multimodal parsing to get the best output.
4. Optimum way to handle the metadata per data source, so that retrieval can be easier.
5. Data encryption before storing and during retrieval, we can use the standard embedding models for embedding till this step.
6. Global, mission based or datasource level context filtering and chat capability.
7. Memory management: In-context memory (recent conversation), Semantic memory (extracted facts and meta data for the user), episodic memory (complete conversation history) 
8. Single user interaction with the assitant at a time.

Milestone 2
1. Support for sensor and other mathematical data: Ability to process sensor data (need to define the sensor data, it's format and data structure) 
2. Advanced Embedding: We will use some fine tuned embedding model to process the sensor data better as compared the 1st milestone.
3. Evaluations
4. 

Milestone 3
1. Multi user interaction
2. Enable Reasoning in the model

##### Test data
1. Public data from ISRO and NASA (Need to research)
2. Mock data/ synthetic data generation, We will not have the actual data from any of the organization.


Such assitant should be intelligent enough to process the data points related to:
1. Trajetory & Flight Dynamics: Altitude/ Velocity/ Accleration, Flight path angle, Downrange distance, Pitch, Yaw, Roll, Orbital elements
2. Propulsion system metrics: Chamber pressure, Thrust and Throttle levels, Fuel/ Oxidizer tank pressure & levels, engine temperature, Gimbal angle.
3. Structural & Mechanical health: Vibrations/ Acceleration (g-force), strain guages, Fariing separation, stage separaion events, pyro/ valve status
4. Guidance, Navigation & Control (GNC): IMU (Inertial Measurement unit) data, Gyroscope and accelerometer readings, attitude control data, Star tracker/ Sun sensor data
5. Electrical and Avionics: Battery voltages and currents, power consumption per subsystem, onboard, computer status, Data bus (CAN, Spacewire)
6. Thermal Management: Component tempratures, Heat flux/ cooling system status, cryogenic tank boil-off rates
7. Telemetry and communication: Signal strength (SNR, link margin), Bit error rate, Uplink command status
8. Range safety & Termination systems: Rocket position relative to flight corridor, FTS (Flight Termination system), Auto abort triggers.
9. Payload Monitoring: separation confirmation, Tumble rate/ spin rate, Initial telemetry satellite

##### Interface
1. Milestone 1: User based 

##### Security Measures
1. Data encryption
2. Encryption at storage level
3. 



#### Unknowns
1. How various type of data stored? What kind of DB are used. 
2. What all kind of data that needs to be processed.







