import proxy

p = proxy.proxy("config.json", "0.0.0.0", 2000)
p.run()