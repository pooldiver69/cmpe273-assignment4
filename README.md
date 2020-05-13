# Consistent Hashing and RHW Hashing

The distributed cache you implemented in the midterm is based on naive modula hashing to shard the data.

## Part I.

Implement Rendezvous hashing to shard the data.

```
python test_rh_client.py
```

example output:
```
...
...
server at 127.0.0.1:4000 cached 23 data
server at 127.0.0.1:4001 cached 35 data
server at 127.0.0.1:4002 cached 24 data
server at 127.0.0.1:4003 cached 24 data
```

## Part II.

Implement consistent hashing to shard the data.

Features:

* Add virtual node layer in the consistent hashing.
* Implement virtual node with data replication. 
