## Boggle Word Game

Problem: Refer to Problem.MD

### Solutions

1. Runtime compute if input is valid, searching adjacent cells for the first character of the input word.
2. Precalculate all valid words on startup / when board is defined. O(1) lookup but potentially huge space usage.

For this project, i will be aiming for simplicity, and will implement the runtime solution.

### Architecture

1. Framework

I have elected to use Python with Django for its batteries included properties, making it relatively quick to setup and deploy.

### 2. Datastore

Options considered

#### A. Stateless, use base64 encoding to store game state entirely.

Pros:

- No management of local state required, least complexity.
- Technically there will be no need for a server at all, clients will be able to maintain their game state by simply backing up the encoded string.

Cons:

- No way to track currently running game states.
- No way to implement solution 2 mentioned above, as server will be stateless.
- Users might be able to game the system by decoding the string, modifying its value, and reencoding it. This can be avoided with encryption.


#### B. Simple in memory data store.

Pros:

- Relatively simple implementation, can even be in memory on the instance itself.
- Can be more performant than solution A, at the very least avoiding performance impact of decoding + reading game states.
- Slighly more extendable, able to add to game state without affecting existing games.

Cons:

- Game state is lost on instance restart.
- Scaling will be an issue, as existing game states will carry over to a new node. Load balancers relying on distributing individual requests will also not work.


#### C. Persistent Storage

Pros:

- The most scalable solution
- Compared to solution A, user is able to recover game state even if they lose their auth token.
- Compared to solution B, there will be no issue with scaling across multiple instances.

Cons:

- Complexity

For the purposes of this project, i will initially start with solution B and transition to solution C after implementation of the algorithm.
