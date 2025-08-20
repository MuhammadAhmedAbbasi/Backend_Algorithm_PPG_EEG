from dataclasses import dataclass, field
from redis import Redis

# 初始化Redis客户端
redis_client = Redis(host='112.124.48.213', port=6379, db=1, password="313521996")

@dataclass
class TokenIdentity:
    _id: int = field(default=None, metadata={"index": True})
    account: str = field(default=None, metadata={"index": True})
    token: str = field(default=None, metadata={"index": True})
    expiration: int = field(default=21600)  # 默认TTL为6h
    
    def save_to_redis(self, redis_client: Redis):
        token_key = f"token:{self.token}"
        redis_client.hmset(
            token_key,
            {
                "account": self.account,
                "token": self.token,
                "expiration": self.expiration,
            },
        )
        redis_client.expire(token_key, self.expiration)

    @classmethod
    def load_from_redis(cls, redis_client: Redis, _id: int):
        token_key = f"token:{_id}"
        token_data = redis_client.hgetall(token_key)
        if token_data:
            return cls(
                _id=_id,
                account=token_data.get(b'account').decode(),
                token=token_data.get(b'token').decode(),
                expiration=int(token_data.get(b'expiration', 21600)),
            )
        return None

# 使用示例
# token = TokenIdentity(_id=1, account="user1", token="abc123", revoked=False, expired=False)
# token.save_to_redis(redis_client)
# loaded_token = TokenIdentity.load_from_redis(redis_client, 1)
