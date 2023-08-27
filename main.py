import userUpdaterBot
import fetchServers
import time

now = time.time()
userDelay = now + (15 * 60)
serverDelay = now + (10 * 60)

fetchServers.main()
userUpdaterBot.main()

while True:
	now = time.time()

	if now > userDelay:
		fetchServers.main()
		serverDelay = now + (10 * 60)
	elif now > serverDelay:
		userUpdaterBot.main()
		userDelay = now + (15 * 60)