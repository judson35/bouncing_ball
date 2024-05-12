import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.integrate import solve_ivp

figure, ax = plt.subplots()

ax.set_xlim(-10, 10)
ax.set_ylim(-1, 11)

class Ball:
    def __init__(self, x : float, y : float, d=10):
        self.x = x
        self.y = y
        self.d = d

        self.c = 0.001
        self.m = 1
        self.Fg = self.m * 9.81
        self.U = np.array([0, -self.Fg])

        self.X = np.array([self.y, 0.00])
        self.A = np.array([[0, 1], [0, -self.c/self.m]])

    def update_state(self, t : float, U=0): # When ball is in air
        self.x = self.x
        self.X_dot = self.A @ self.X + self.U
        return self.X_dot
    
    # def update_state_2(self, t : float, U=0): # When ball is on ground
    #     self.x = self.x
    #     self.X_dot = self.A @ self.X + self.U + np.array([0, 100])
    #     return self.X_dot
    
    def hit_ground(self, t, X):
        if X[0] <= 0:
            self.U = np.array([0, -self.Fg + 100])
        return X[0]

if __name__ == "__main__":
    X0 = [10.0, 0.0]
    t0 = 0
    tf = 10
    dt = 0.01
    t = np.linspace(t0, tf, int((tf - t0)/dt))
    ball = Ball(0.0, X0[0], 10)
    ON_GROUND = False

    def hit_ground(t, X):
        if X[0] <= 0.01:
            ON_GROUND = True
            ball.U = np.array([0, -ball.Fg + 100])
            print("Hit ground")
        return X[0]

    def leave_ground(t, X):
        if X[0] >= 0 and ON_GROUND:
            ball.U = np.array([0, -ball.Fg])
            print(f"ON_GROUND = {ON_GROUND} \tLeave ground")
        return X[0]
    
    hit_ground.terminal = False
    # hit_ground.direction = 1.0

    leave_ground.terminal = False
    # leave_ground.direction = -1.0

    sol = solve_ivp(ball.update_state, [t0, tf], X0, method='RK45', t_eval=t, events=[hit_ground, leave_ground])

    b, = ax.plot(ball.x, ball.y, color='red', marker=".", markersize=10)

    def animation_function(i):

        b.set_xdata(ball.x)
        b.set_ydata(sol.y[0, i])

        return b,

    animation = FuncAnimation(figure, func=animation_function, frames=np.array([i for i in range(len(t))]), interval=int(1/dt))
    plt.show()
