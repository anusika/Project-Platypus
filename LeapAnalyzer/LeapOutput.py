################################################################################
# Copyright (C) 2012-2013 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################

from itertools import cycle
import os, sys, inspect
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
#Windows
lib_dir = os.path.abspath(os.path.join(src_dir, '../lib_windows'))

#Mac 
#lib_dir2 = os.path.abspath(os.path.join(src_dir, '../lib_mac'))
sys.path.insert(0, lib_dir)
#sys.path.insert(0, lib_dir2)
import Leap, sys, thread, time, math
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_ START', 'STATE_UPDATE', 'STATE_END']

    # Hands are steady if the movements don't vary by 50mm (5cm)
    STEADY_HANDS = 35
    
    # Frame by frame of each hand and its movements
    hand_actions = []

    def clear_hand_actions(self):
        hand_actions = []

    def pack(self, hand):
        ret = []
        ret.append(hand.palm_position[0] * 0.001)
        ret.append(hand.palm_position[1] * 0.001)
        ret.append(hand.palm_position[2] * 0.001)
        ret.append(hand.palm_normal.roll * Leap.RAD_TO_DEG)
        if ret[len(ret) - 1] > 90:
            ret[len(ret) - 1] = 90
        elif ret[len(ret) - 1] < -90:
            ret[len(ret) - 1] = -90

        ret.append(hand.direction.pitch * Leap.RAD_TO_DEG)
        if ret[len(ret) - 1] > 90:
            ret[len(ret) - 1] = 90
        elif ret[len(ret) - 1] < -90:
            ret[len(ret) - 1] = -90

        ret.append(hand.direction.yaw * Leap.RAD_TO_DEG)

        #Thumb, forefinger, middle, ring, little
        ret.append(None)
        ret.append(None)
        ret.append(None)
        ret.append(None)
        ret.append(None)
        return ret

    def wait_for_steadiness(self, controller, frames_to_wait):
        recording = []
        while len(controller.frame().hands) != 2:
            print(len(controller.frame().hands))
            continue
        frame = controller.frame()
        initial_positions = [frame.hands[0].palm_position, frame.hands[1].palm_position]
        last_id = frame.id
        
        index = 1

        while(index < frames_to_wait):
            time.sleep(0.01)
            new_frame = controller.frame()
            if new_frame.id != last_id:
                print(index)
                last_id = new_frame.id
                hands = new_frame.hands
                # L, then Right
                if hands[0].is_left:
                    recording.append(self.pack(hands[0]) + self.pack(hands[1]))
                else:
                    recording.append(self.pack(hands[1]) + self.pack(hands[0]))

                if len(hands) != 2:
                    # have to reset
                    recording = []
                    initial_positions = None
                    last_id = None
                    index = 0
                    continue
                elif initial_positions == None:
                    # means we reset earlier
                    initial_positions = [hands[0].palm_position, hands[1].palm_position]
                    index = 1
                    continue
                elif (abs(initial_positions[0][0] - hands[0].palm_position[0]) > self.STEADY_HANDS or
                    abs(initial_positions[0][1] - hands[0].palm_position[1]) > self.STEADY_HANDS or
                    abs(initial_positions[0][2] - hands[0].palm_position[2]) > self.STEADY_HANDS or
                    abs(initial_positions[1][0] - hands[1].palm_position[0]) > self.STEADY_HANDS or
                    abs(initial_positions[1][1] - hands[1].palm_position[1]) > self.STEADY_HANDS or
                    abs(initial_positions[1][2] - hands[1].palm_position[2]) > self.STEADY_HANDS):
                    # have to reset
                    initial_positions = [hands[0].palm_position, hands[1].palm_position]
                    if index > 10: # give some allowance/buffer for resetting the recording.
                        recording = []
                    index = 1
                else:
                    index += 1
        return recording

    def record(self, controller):
        self.wait_for_steadiness(controller, 150)
        # steady, now start recording
        recording = self.wait_for_steadiness(controller, 150)
        truncated_recording = recording[0:len(recording) - 150]
        return self.resize_to_136(truncated_recording)

    def resize_to_136(self, frames):
        length = len(frames)
        if len(frames) < 136:
            while len(frames) < 136:
                frames.append(frames[-1:])
        else:
            difference = length - 136
            delete_every = int(math.floor(length / difference))
            index = delete_every
            while index < len(frames):
                del frames[index]
                index += delete_every
            while len(frames) > 136:
                frames = frames[:-1]
            while len(frames) < 136:
                frames.append(frames[-1:])

        return frames

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

        # Disabled gestures
        # controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        # controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        # controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        #Get the most recent frame and report some basic information
        frame = controller.frame()

        hands = frame.hands
        if len(hands) != 2:
            return
        
        print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d" % (
              frame.id, frame.timestamp, len(frame.hands), len(frame.fingers))

        # Get hands
        for hand in frame.hands:

            handType = "Left hand" if hand.is_left else "Right hand"
	
            print "  %s, id %d, position: %s" % (
                handType, hand.id, hand.palm_position)

            # Get the hand's normal vector and direction
            normal = hand.palm_normal
            direction = hand.direction

            # Calculate the hand's pitch, roll, and yaw angles
            print "  pitch: %f degrees, roll: %f degrees, yaw: %f degrees" % (
                direction.pitch * Leap.RAD_TO_DEG,
                normal.roll * Leap.RAD_TO_DEG,
                direction.yaw * Leap.RAD_TO_DEG)

            # Get fingers
            for finger in hand.fingers:
									
				proximal = finger.bone(1)
				distal = finger.bone(3)
				dot = proximal.direction.dot(distal.direction)
				flexed = 1.0 - (1.0 + dot) / 2.0
				
				print " %s finger, flexed: %f" % (
					self.finger_names[finger.type],
					flexed)
	
	
                # print "    %s finger, id: %d, length: %fmm, width: %fmm" % (
                #     self.finger_names[finger.type],
                #     finger.id,
                #     finger.length,
                #     finger.width)

                # # Get bones
                # for b in range(0, 4):
                #     bone = finger.bone(b)
                #     print "      Bone: %s, start: %s, end: %s, direction: %s" % (
                #         self.bone_names[bone.type],
                #         bone.prev_joint,
                #         bone.next_joint,
                #         bone.direction)

def calibrate(self, frame):
    hands = frame.hands
    # set (x,y,z) for both hands to (0,0,0)
    if len(hand) != 2:
        raise Error("Needs two hands")
    else:
        return [[-hands[0].palm_position[0], -hands[0].palm_position[1], -hands[0].palm_position[2],
                [-hands[1].palm_position[0], -hands[1].palm_position[1], -hands[1].palm_position[2]]]]


calibration = None


def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)
    recording = listener.record(controller)
    print(len(recording))
    # print(recording)
    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()
