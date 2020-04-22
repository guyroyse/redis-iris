const Redis = require("ioredis")
const redis = new Redis()

async function main() {
  let input = [5.0, 3.4, 1.6, 0.4, 6.3, 3.4, 5.6, 2.4]
  await redis.call('ai.tensorset', ['iris_in', 'FLOAT', 2, 4, 'VALUES', ...input])
  await redis.call('ai.modelrun', [ 'iris', 'INPUTS', 'iris_in', 'OUTPUTS', 'iris_out:1', 'iris_out:2'])
  let output = await redis.call('ai.tensorget', ['iris_out:1', 'values'])
  console.log(output)
  await redis.quit()
}

main()
