create table DetectedAnomalies
(
    iDetectedAnomalies int auto_increment
        primary key,
    latitude           float(8, 5) not null,
    longitude          float(8, 5) not null,
    count              int         not null
);

create table PointsAnomalies
(
    iPointsAnomalies int auto_increment
        primary key,
    latitude         float(8, 5) not null,
    longitude        float(8, 5) not null
);

create table Rides
(
    iRide          int auto_increment
        primary key,
    gender         varchar(10)                       not null,
    age            varchar(10)                       not null,
    processedState varchar(20) default 'Unprocessed' not null
);

create table Points
(
    iPoint    int auto_increment
        primary key,
    ride      int                                 not null,
    latitude  float(9, 6)                         not null,
    longitude float(9, 6)                         not null,
    date      timestamp default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP,
    constraint Points_Rides_iRide_fk
        foreign key (ride) references Rides (iRide)
);

create table Accelerations
(
    iAcceleration     int auto_increment
        primary key,
    ride              int         not null,
    endPoint          int         not null,
    accelerationValue float(9, 3) not null,
    constraint Accelerations_Points_iPoints_fk
        foreign key (endPoint) references Points (iPoint),
    constraint Accelerations_Rides_iRide_fk
        foreign key (ride) references Rides (iRide)
);

create table AccelerationsPreProcessed
(
    iAccelerationPreProcessed int auto_increment
        primary key,
    ride                      int         not null,
    endPoint                  int         not null,
    accelerationValue         float(9, 3) null,
    constraint AccelerationsPreProcessed_Points_iPoints_fk
        foreign key (endPoint) references Points (iPoint),
    constraint AccelerationsPreProcessed_Rides_iRide_fk
        foreign key (ride) references Rides (iRide)
);

create table Anomalies
(
    iAnomaly          int auto_increment
        primary key,
    ride              int         not null,
    point             int         not null,
    accelerationValue float(9, 3) not null,
    constraint Anomalies_Points_iPoints_fk
        foreign key (point) references Points (iPoint),
    constraint Anomalies_Rides_iRide_fk
        foreign key (ride) references Rides (iRide)
);

