import wpilib
import wpilib.drive
from wpilib.drive import *
import rev


class MyRobot(wpilib.TimedRobot):

    def robotInit(self):
        """Robot initialization function"""
        wpilib.CameraServer.launch()
        self.frontLeftMotor = rev.CANSparkMax(1, rev._rev.CANSparkMaxLowLevel.MotorType.kBrushless)
        self.frontRightMotor = rev.CANSparkMax(2, rev._rev.CANSparkMaxLowLevel.MotorType.kBrushless)
        self.rearLeftMotor = rev.CANSparkMax(3, rev._rev.CANSparkMaxLowLevel.MotorType.kBrushless)
        self.rearRightMotor = rev.CANSparkMax(4, rev._rev.CANSparkMaxLowLevel.MotorType.kBrushless)
        #self.Shooter = rev.CANSparkMax(7, rev._rev.CANSparkMaxLowLevel.MotorType.kBrushless)
        self.arm = rev.CANSparkMax(8, rev._rev.CANSparkMaxLowLevel.MotorType.kBrushless)
        self.Intake = wpilib.Spark(1)
        


        self.left = wpilib.SpeedControllerGroup(self.frontLeftMotor, self.rearLeftMotor)
        self.right = wpilib.SpeedControllerGroup(self.frontRightMotor, self.rearRightMotor)

        self.myRobot = DifferentialDrive(self.left, self.right)
        self.timer= wpilib.Timer()
        self.myRobot.setExpiration(0.1)

        # joysticks 1 & 2 on the driver station
        self.driver = wpilib.Joystick(0)
        self.manip = wpilib.Joystick(1)

    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""
        self.timer.reset()
        self.timer.start()

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""

        # Drive for two seconds
        speed= -.5
        if self.timer.get() < 2.0:
            self.Intake.set(1)  # shoot
        elif self.timer.get() < 4.0:
            self.myRobot.tankDrive(speed, speed*-1)  # Drive backwards at half speed
            self.Intake.set(0)
        else:
            self.myRobot.tankDrive(0, 0)  # Stop robot
            self.Intake.set(0)

    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        """Runs the motors with tank steering"""

        self.myRobot.tankDrive(self.driver.getRawAxis(1)*-0.5, self.driver.getRawAxis(5) * .5, False)
        self.arm.set(self.manip.getRawAxis(1)*-0.5)

        if self.manip.getRawButton(1) or self.manip.getRawButton(2):
            if self.manip.getRawButton(1):
                self.Intake.set(1)
            else:
                self.Intake.set(-1)
        else:
            self.Intake.set(0)


if __name__ == "__main__":
    wpilib.run(MyRobot)