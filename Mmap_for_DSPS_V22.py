# k3nny's Python mapping of The Iron Wolf's rF2 Shared Memory Tools
# https://github.com/TheIronWolfModding/rF2SharedMemoryMapPlugin
# https://forum.studio-397.com/index.php?members/k3nny.35143/
# Some of the original comments from ISI/S392's InternalsPlugin.hpp
# restored.
# https://www.studio-397.com/wp-content/uploads/2016/12/rF2-Example-Plugin-7.7z

import mmap
import ctypes
import time

MAX_MAPPED_VEHICLES = 128
MAX_MAPPED_IDS = 512


class rF2Vec3(ctypes.Structure):
    _pack_ = 4
    _fields_ = [
        ('x', ctypes.c_double),
        ('y', ctypes.c_double),
        ('z', ctypes.c_double),
    ]

class TelemWheelV01(ctypes.Structure):
    _pack_ = 4
    _fields_ = [
        ('mSuspensionDeflection', ctypes.c_double),               # metres
        ('mRideHeight', ctypes.c_double),                         # metres
        ('mSuspForce', ctypes.c_double),                          # pushrod load in Newtons
        ('mBrakeTemp', ctypes.c_double),                          # Celsius
        ('mBrakePressure', ctypes.c_double),                      # currently 0.0-1.0, depending on driver input and brake balance; will convert to true brake pressure (kPa) in future

        ('mRotation', ctypes.c_double),                           # radians/sec
        ('mLateralPatchVel', ctypes.c_double),                    # lateral velocity at contact patch
        ('mLongitudinalPatchVel', ctypes.c_double),               # longitudinal velocity at contact patch
        ('mLateralGroundVel', ctypes.c_double),                   # lateral velocity at contact patch
        ('mLongitudinalGroundVel', ctypes.c_double),              # longitudinal velocity at contact patch
        ('mCamber', ctypes.c_double),                             # radians (positive is left for left-side wheels, right for right-side wheels)
        ('mLateralForce', ctypes.c_double),                       # Newtons
        ('mLongitudinalForce', ctypes.c_double),                  # Newtons
        ('mTireLoad', ctypes.c_double),                           # Newtons

        ('mGripFract', ctypes.c_double),                          # an approximation of what fraction of the contact patch is sliding
        ('mPressure', ctypes.c_double),                           # kPa (tire pressure)
        ('mTemperature', ctypes.c_double*3),                      # Kelvin (subtract 273.15 to get Celsius), left/center/right (not to be confused with inside/center/outside!)
        ('mWear', ctypes.c_double),                               # wear (0.0-1.0, fraction of maximum) ... this is not necessarily proportional with grip loss
        ('mTerrainName', ctypes.c_ubyte*16),                      # the material prefixes from the TDF file
        ('mSurfaceType', ctypes.c_ubyte),                         # 0=dry, 1=wet, 2=grass, 3=dirt, 4=gravel, 5=rumblestrip, 6=special
        ('mFlat', ctypes.c_ubyte),                                # whether tire is flat
        ('mDetached', ctypes.c_ubyte),                            # whether wheel is detached

        ('mVerticalTireDeflection', ctypes.c_double),             # how much is tire deflected from its (speed-sensitive) radius
        ('mWheelYLocation', ctypes.c_double),                     # wheel's y location relative to vehicle y location
        ('mToe', ctypes.c_double),                                # current toe angle w.r.t. the vehicle

        ('mTireCarcassTemperature', ctypes.c_double),             # rough average of temperature samples from carcass (Kelvin)
        ('mTireInnerLayerTemperature', ctypes.c_double*3),        # rough average of temperature samples from innermost layer of rubber (before carcass) (Kelvin)
        ('mExpansion', ctypes.c_ubyte*24),
    ]


class rF2VehicleTelemetry(ctypes.Structure):
    _pack_ = 4
    _fields_ = [
        # Time
        ('mID', ctypes.c_int),                                    # slot ID (note that it can be re-used in multiplayer after someone leaves)
        ('mDeltaTime', ctypes.c_double),                          # time since last update (seconds)
        ('mElapsedTime', ctypes.c_double),                        # game session time
        ('mLapNumber', ctypes.c_int),                             # current lap number
        ('mLapStartET', ctypes.c_double),                         # time this lap was started
        ('mVehicleName', ctypes.c_ubyte*64),                      # current vehicle name
        ('mTrackName', ctypes.c_ubyte*64),                        # current track name

        # Position and derivatives
        ('mPos', rF2Vec3),                                        # world position in metres
        ('mLocalVel', rF2Vec3),                                   # velocity (metres/sec) in local vehicle coordinates
        ('mLocalAccel', rF2Vec3),                                 # acceleration (metres/sec^2) in local vehicle coordinates

        # Orientation and derivatives
        ('mOri', rF2Vec3*3),                                      # rows of orientation matrix (use TelemQuat conversions if desired), also converts local
                                                                  # vehicle vectors into world X, Y, or Z using dot product of rows 0, 1, or 2 respectively
        ('mLocalRot', rF2Vec3),                                   # rotation (radians/sec) in local vehicle coordinates
        ('mLocalRotAccel', rF2Vec3),                              # rotational acceleration (radians/sec^2) in local vehicle coordinates

        # Vehicle status
        ('mGear', ctypes.c_int),                                  # -1=reverse, 0=neutral, 1+=forward gears
        ('mEngineRPM', ctypes.c_double),                          # engine RPM
        ('mEngineWaterTemp', ctypes.c_double),                    # Celsius
        ('mEngineOilTemp', ctypes.c_double),                      # Celsius
        ('mClutchRPM', ctypes.c_double),                          # clutch RPM

        # Driver input
        ('mUnfilteredThrottle', ctypes.c_double),                 # ranges  0.0-1.0
        ('mUnfilteredBrake', ctypes.c_double),                    # ranges  0.0-1.0
        ('mUnfilteredSteering', ctypes.c_double),                 # ranges -1.0-1.0 (left to right)
        ('mUnfilteredClutch', ctypes.c_double),                   # ranges  0.0-1.0

        # Filtered input (various adjustments for rev or speed limiting, TC, ABS?, speed sensitive steering, clutch work for semi-automatic shifting, etc.)
        ('mFilteredThrottle', ctypes.c_double),                   # ranges  0.0-1.0
        ('mFilteredBrake', ctypes.c_double),                      # ranges  0.0-1.0
        ('mFilteredSteering', ctypes.c_double),                   # ranges -1.0-1.0 (left to right)
        ('mFilteredClutch', ctypes.c_double),                     # ranges  0.0-1.0

        # Misc
        ('mSteeringShaftTorque', ctypes.c_double),                # torque around steering shaft (used to be mSteeringArmForce, but that is not necessarily accurate for feedback purposes)
        ('mFront3rdDeflection', ctypes.c_double),                 # deflection at front 3rd spring
        ('mRear3rdDeflection', ctypes.c_double),                  # deflection at rear 3rd spring

        # Aerodynamics
        ('mFrontWingHeight', ctypes.c_double),                    # front wing height
        ('mFrontRideHeight', ctypes.c_double),                    # front ride height
        ('mRearRideHeight', ctypes.c_double),                     # rear ride height
        ('mDrag', ctypes.c_double),                               # drag
        ('mFrontDownforce', ctypes.c_double),                     # front downforce
        ('mRearDownforce', ctypes.c_double),                      # rear downforce

        # State/damage info
        ('mFuel', ctypes.c_double),                               # amount of fuel (litres)
        ('mEngineMaxRPM', ctypes.c_double),                       # rev limit
        ('mScheduledStops', ctypes.c_ubyte),                      # number of scheduled pitstops
        ('mOverheating', ctypes.c_ubyte),                         # whether overheating icon is shown
        ('mDetached', ctypes.c_ubyte),                            # whether any parts (besides wheels) have been detached
        ('mHeadlights', ctypes.c_ubyte),                          # whether headlights are on
        ('mDentSeverity', ctypes.c_ubyte*8),                      # dent severity at 8 locations around the car (0=none, 1=some, 2=more)
        ('mLastImpactET', ctypes.c_double),                       # time of last impact
        ('mLastImpactMagnitude', ctypes.c_double),                # magnitude of last impact
        ('mLastImpactPos', rF2Vec3),                              # location of last impact

        # Expanded
        ('mEngineTorque', ctypes.c_double),                       # current engine torque (including additive torque) (used to be mEngineTq, but there's little reason to abbreviate it)
        ('mCurrentSector', ctypes.c_int),                         # the current sector (zero-based) with the pitlane stored in the sign bit (example: entering pits from third sector gives 0x80000002)
        ('mSpeedLimiter', ctypes.c_ubyte),                        # whether speed limiter is on
        ('mMaxGears', ctypes.c_ubyte),                            # maximum forward gears
        ('mFrontTireCompoundIndex', ctypes.c_ubyte),              # index within brand
        ('mRearTireCompoundIndex', ctypes.c_ubyte),               # index within brand
        ('mFuelCapacity', ctypes.c_double),                       # capacity in litres
        ('mFrontFlapActivated', ctypes.c_ubyte),                  # whether front flap is activated
        ('mRearFlapActivated', ctypes.c_ubyte),                   # whether rear flap is activated
        ('mRearFlapLegalStatus', ctypes.c_ubyte),                 # 0=disallowed, 1=criteria detected but not allowed quite yet, 2=allowed
        ('mIgnitionStarter', ctypes.c_ubyte),                     # 0=off 1=ignition 2=ignition+starter

        ('mFrontTireCompoundName', ctypes.c_ubyte*18),            # name of front tire compound
        ('mRearTireCompoundName', ctypes.c_ubyte*18),             # name of rear tire compound

        ('mSpeedLimiterAvailable', ctypes.c_ubyte),               # whether speed limiter is available
        ('mAntiStallActivated', ctypes.c_ubyte),                  # whether (hard) anti-stall is activated
        ('mUnused', ctypes.c_ubyte*2),                            #
        ('mVisualSteeringWheelRange', ctypes.c_float),            # the *visual* steering wheel range

        ('mRearBrakeBias', ctypes.c_double),                      # fraction of brakes on rear
        ('mTurboBoostPressure', ctypes.c_double),                 # current turbo boost pressure if available
        ('mPhysicsToGraphicsOffset', ctypes.c_float*3),           # offset from static CG to graphical center
        ('mPhysicalSteeringWheelRange', ctypes.c_float),          # the *physical* steering wheel range

        # Future use
        ('mExpansion', ctypes.c_ubyte*152),       

        # keeping this at the end of the structure to make it easier to replace in future versions
        ('mWheels', TelemWheelV01*4),       
    ]


class rF2Telemetry(ctypes.Structure):
    _pack_ = 4
    _fields_ = [
        ('mVersionUpdateBegin', ctypes.c_uint),
        ('mVersionUpdateEnd', ctypes.c_uint),
        ('mBytesUpdatedHint', ctypes.c_int),
        ('mNumVehicles', ctypes.c_int),
        ('mVehicles', rF2VehicleTelemetry*MAX_MAPPED_VEHICLES),
    ]


class rF2ScoringInfo(ctypes.Structure):
    _pack_ = 4
    _fields_ = [
        ('mTrackName', ctypes.c_ubyte*64),                        # current track name
        ('mSession', ctypes.c_int),                               # current session (0=testday 1-4=practice 5-8=qual 9=warmup 10-13=race)
        ('mCurrentET', ctypes.c_double),                          # current time
        ('mEndET', ctypes.c_double),                              # ending time
        ('mMaxLaps', ctypes.c_int),                               # maximum laps
        ('mLapDist', ctypes.c_double),                            # distance around track
        ('pResultsStream', ctypes.c_ubyte*8),                     # results stream additions since last update (newline-delimited and NULL-terminated)
        ('mNumVehicles', ctypes.c_int),                           # current number of vehicles
                                                                  # Game phases:
                                                                  # 0 Before session has begun
                                                                  # 1 Reconnaissance laps (race only)
                                                                  # 2 Grid walk-through (race only)
                                                                  # 3 Formation lap (race only)
                                                                  # 4 Starting-light countdown has begun (race only)
                                                                  # 5 Green flag
                                                                  # 6 Full course yellow / safety car
                                                                  # 7 Session stopped
                                                                  # 8 Session over
        ('mGamePhase', ctypes.c_ubyte),       
                                                                  # Yellow flag states (applies to full-course only)
                                                                  # -1 Invalid
                                                                  #  0 None
                                                                  #  1 Pending
                                                                  #  2 Pits closed
                                                                  #  3 Pit lead lap
                                                                  #  4 Pits open
                                                                  #  5 Last lap
                                                                  #  6 Resume
                                                                  #  7 Race halt (not currently used)
        ('mYellowFlagState', ctypes.c_byte),
        ('mSectorFlag', ctypes.c_byte*3),                         # whether there are any local yellows at the moment in each sector (not sure if sector 0 is first or last, so test)
        ('mStartLight', ctypes.c_ubyte),                          # start light frame (number depends on track)
        ('mNumRedLights', ctypes.c_ubyte),                        # number of red lights in start sequence
        ('mInRealtime', ctypes.c_ubyte),                          # in realtime as opposed to at the monitor
        ('mPlayerName', ctypes.c_ubyte*32),                       # player name (including possible multiplayer override)
        ('mPlrFileName', ctypes.c_ubyte*64),                      # may be encoded to be a legal filename
        ('mDarkCloud', ctypes.c_double),                          # cloud darkness? 0.0-1.0
        ('mRaining', ctypes.c_double),                            # raining severity 0.0-1.0
        ('mAmbientTemp', ctypes.c_double),                        # temperature (Celsius)
        ('mTrackTemp', ctypes.c_double),                          # temperature (Celsius)
        ('mWind', rF2Vec3),                                       # wind speed
        ('mMinPathWetness', ctypes.c_double),                     # minimum wetness on main path 0.0-1.0
        ('mMaxPathWetness', ctypes.c_double),                     # maximum wetness on main path 0.0-1.0
        ('mExpansion', ctypes.c_ubyte*256),                       # Future use
        ('pVehicleScoringInfoV01', ctypes.c_ubyte*8),       
    ]


class rF2VehicleScoring(ctypes.Structure):
    _pack_ = 4
    _fields_ = [
        ('mID', ctypes.c_int),                                    # slot ID (note that it can be re-used in multiplayer after someone leaves)
        ('mDriverName', ctypes.c_ubyte*32),                       # driver name
        ('mVehicleName', ctypes.c_ubyte*64),                      # vehicle name
        ('mTotalLaps', ctypes.c_short),                           # laps completed
        ('mSector', ctypes.c_byte),                               # 0=sector3, 1=sector1, 2=sector2 (don't ask why)
        ('mFinishStatus', ctypes.c_byte),                         # 0=none, 1=finished, 2=dnf, 3=dq
        ('mLapDist', ctypes.c_double),                            # current distance around track
        ('mPathLateral', ctypes.c_double),                        # lateral position with respect to *very approximate* "center" path
        ('mTrackEdge', ctypes.c_double),                          # track edge (w.r.t. "center" path) on same side of track as vehicle

        ('mBestSector1', ctypes.c_double),                        # best sector 1
        ('mBestSector2', ctypes.c_double),                        # best sector 2 (plus sector 1)
        ('mBestLapTime', ctypes.c_double),                        # best lap time
        ('mLastSector1', ctypes.c_double),                        # last sector 1
        ('mLastSector2', ctypes.c_double),                        # last sector 2 (plus sector 1)
        ('mLastLapTime', ctypes.c_double),                        # last lap time
        ('mCurSector1', ctypes.c_double),                         # current sector 1 if valid
        ('mCurSector2', ctypes.c_double),                         # current sector 2 (plus sector 1) if valid
        # no current laptime because it instantly becomes "last"

        ('mNumPitstops', ctypes.c_short),                         # number of pitstops made
        ('mNumPenalties', ctypes.c_short),                        # number of outstanding penalties
        ('mIsPlayer', ctypes.c_ubyte),                            # is this the player's vehicle

        ('mControl', ctypes.c_byte),                              # who's in control: -1=nobody (shouldn't get this), 0=local player, 1=local AI, 2=remote, 3=replay (shouldn't get this)
        ('mInPits', ctypes.c_ubyte),                              # between pit entrance and pit exit (not always accurate for remote vehicles)
        ('mPlace', ctypes.c_ubyte),                               # 1-based position
        ('mVehicleClass', ctypes.c_ubyte*32),                     # vehicle class


        ('mTimeBehindNext', ctypes.c_double),                     # time behind vehicle in next higher place
        ('mLapsBehindNext', ctypes.c_int),                        # laps behind vehicle in next higher place
        ('mTimeBehindLeader', ctypes.c_double),                   # time behind leader
        ('mLapsBehindLeader', ctypes.c_int),                      # laps behind leader
        ('mLapStartET', ctypes.c_double),                         # time this lap was started


        ('mPos', rF2Vec3),                                        # world position in metres
        ('mLocalVel', rF2Vec3),                                   # velocity (metres/sec) in local vehicle coordinates
        ('mLocalAccel', rF2Vec3),                                 # acceleration (metres/sec^2) in local vehicle coordinates


        ('mOri', rF2Vec3*3),                                      # rows of orientation matrix (use TelemQuat conversions if desired), also converts local
                                                                  # vehicle vectors into world X, Y, or Z using dot product of rows 0, 1, or 2 respectively
        ('mLocalRot', rF2Vec3),                                   # rotation (radians/sec) in local vehicle coordinates
        ('mLocalRotAccel', rF2Vec3),                              # rotational acceleration (radians/sec^2) in local vehicle coordinates

        # tag.2012.03.01 - stopped casting some of these so variables now have names and mExpansion has shrunk, overall size and old data locations should be same
        ('mHeadlights', ctypes.c_ubyte),                          # status of headlights
        ('mPitState', ctypes.c_ubyte),                            # 0=none, 1=request, 2=entering, 3=stopped, 4=exiting
        ('mServerScored', ctypes.c_ubyte),                        # whether this vehicle is being scored by server (could be off in qualifying or racing heats)
        ('mIndividualPhase', ctypes.c_ubyte),                     # game phases (described below) plus 9=after formation, 10=under yellow, 11=under blue (not used)

        ('mQualification', ctypes.c_int),                         # 1-based, can be -1 when invalid

        ('mTimeIntoLap', ctypes.c_double),                        # estimated time into lap
        ('mEstimatedLapTime', ctypes.c_double),                   # estimated laptime used for 'time behind' and 'time into lap' (note: this may changed based on vehicle and setup!?)
        ('mPitGroup', ctypes.c_ubyte*24),        
                                                                  # pit group (same as team name unless pit is shared)
        ('mFlag', ctypes.c_ubyte),                                # primary flag being shown to vehicle (currently only 0=green or 6=blue)
        ('mUnderYellow', ctypes.c_ubyte),                         # whether this car has taken a full-course caution flag at the start/finish line
        ('mCountLapFlag', ctypes.c_ubyte),                        # 0 = do not count lap or time, 1 = count lap but not time, 2 = count lap and time
        ('mInGarageStall', ctypes.c_ubyte),                       # appears to be within the correct garage stall

        ('mUpgradePack', ctypes.c_ubyte*16),                      # Coded upgrades
        ('mExpansion', ctypes.c_ubyte*60),        
    ]


class rF2Scoring(ctypes.Structure):
    _pack_ = 4
    _fields_ = [
        ('mVersionUpdateBegin', ctypes.c_uint),
        ('mVersionUpdateEnd', ctypes.c_uint),
        ('mBytesUpdatedHint', ctypes.c_int),
        ('mScoringInfo', rF2ScoringInfo),
        ('mVehicles', rF2VehicleScoring*MAX_MAPPED_VEHICLES),
    ]

class rF2PhysicsOptions(ctypes.Structure):
    _pack_ = 4
    _fields_ = [
        ('mTractionControl', ctypes.c_ubyte),                     # 0 (off) - 3 (high)
        ('mAntiLockBrakes', ctypes.c_ubyte),                      # 0 (off) - 2 (high)
        ('mStabilityControl', ctypes.c_ubyte),                    # 0 (off) - 2 (high)
        ('mAutoShift', ctypes.c_ubyte),                           # 0 (off), 1 (upshifts), 2 (downshifts), 3 (all)
        ('mAutoClutch', ctypes.c_ubyte),                          # 0 (off), 1 (on)
        ('mInvulnerable', ctypes.c_ubyte),                        # 0 (off), 1 (on)
        ('mOppositeLock', ctypes.c_ubyte),                        # 0 (off), 1 (on)
        ('mSteeringHelp', ctypes.c_ubyte),                        # 0 (off) - 3 (high)
        ('mBrakingHelp', ctypes.c_ubyte),                         # 0 (off) - 2 (high)
        ('mSpinRecovery', ctypes.c_ubyte),                        # 0 (off), 1 (on)
        ('mAutoPit', ctypes.c_ubyte),                             # 0 (off), 1 (on)
        ('mAutoLift', ctypes.c_ubyte),                            # 0 (off), 1 (on)
        ('mAutoBlip', ctypes.c_ubyte),                            # 0 (off), 1 (on)
        ('mFuelMult', ctypes.c_ubyte),                            # fuel multiplier (0x-7x)
        ('mTireMult', ctypes.c_ubyte),                            # tire wear multiplier (0x-7x)
        ('mMechFail', ctypes.c_ubyte),                            # mechanical failure setting; 0 (off), 1 (normal), 2 (timescaled)
        ('mAllowPitcrewPush', ctypes.c_ubyte),                    # 0 (off), 1 (on)
        ('mRepeatShifts', ctypes.c_ubyte),                        # accidental repeat shift prevention (0-5; see PLR file)
        ('mHoldClutch', ctypes.c_ubyte),                          # for auto-shifters at start of race: 0 (off), 1 (on)
        ('mAutoReverse', ctypes.c_ubyte),                         # Whether shifting up and down simultaneously equals neutral
        ('mAlternateNeutral', ctypes.c_ubyte),                    # 0 (off), 1 (on)
        ('mAIControl', ctypes.c_ubyte),                           # Whether player vehicle is currently under AI control
        ('mUnused1', ctypes.c_ubyte),
        ('mUnused2', ctypes.c_ubyte),
        ('mManualShiftOverrideTime', ctypes.c_float),             # time before auto-shifting can resume after recent manual shift
        ('mAutoShiftOverrideTime', ctypes.c_float),               # time before manual shifting can resume after recent auto shift
        ('mSpeedSensitiveSteering', ctypes.c_float),              # 0.0 (off) - 1.0
        ('mSteerRatioSpeed', ctypes.c_float),                     # speed (m/s) under which lock gets expanded to full
    ]

class rF2TrackedDamage(ctypes.Structure):
    _pack_ = 4
    _fields_ = [
        ('mMaxImpactMagnitude', ctypes.c_double),
        ('mAccumulatedImpactMagnitude', ctypes.c_double),
    ]

class rF2VehScoringCapture(ctypes.Structure):
    _pack_ = 4
    _fields_ = [
        ('mID', ctypes.c_int),
        ('mPlace', ctypes.c_ubyte),
        ('mIsPlayer', ctypes.c_ubyte),
        ('mFinishStatus', ctypes.c_byte),
    ]

class rF2SessionTransitionCapture(ctypes.Structure):
    _pack_ = 4
    _fields_ = [
        ('mGamePhase', ctypes.c_ubyte),
        ('mSession', ctypes.c_int),
        ('mNumScoringVehicles', ctypes.c_int),
        ('mScoringVehicles', rF2VehScoringCapture*MAX_MAPPED_VEHICLES),
    ]

class rF2HostedPluginVars(ctypes.Structure):
    _pack_ = 4
    _fields_ = [
        ('StockCarRules_IsHosted', ctypes.c_ubyte),
        ('StockCarRules_DoubleFileType', ctypes.c_int),
    ]


class rF2Extended(ctypes.Structure):
    _pack_ = 4
    _fields_ = [
        ('mVersionUpdateBegin', ctypes.c_uint),
        ('mVersionUpdateEnd', ctypes.c_uint),
        ('mVersion', ctypes.c_ubyte*8),
        ('is64bit', ctypes.c_ubyte),
        ('mPhysics', rF2PhysicsOptions),
        ('mTrackedDamages', rF2TrackedDamage*MAX_MAPPED_IDS),
        ('mInRealtimeFC', ctypes.c_ubyte),                        # 1: on track
        ('mMultimediaThreadStarted', ctypes.c_ubyte),
        ('mSimulationThreadStarted', ctypes.c_ubyte),
        ('mSessionStarted', ctypes.c_ubyte),                      # 1: track loaded
        ('mTicksSessionStarted', ctypes.c_longlong),
        ('mTicksSessionEnded', ctypes.c_longlong),
        ('mSessionTransitionCapture',rF2SessionTransitionCapture ),
        ('mDisplayedMessageUpdateCapture', ctypes.c_ubyte*128),
        ('mHostedPluginVars', rF2HostedPluginVars),
    ]


class SimInfo:
    def __init__(self):


        self._rf2_tele = mmap.mmap(0, ctypes.sizeof(rF2Telemetry), "$rFactor2SMMP_Telemetry$")
        self.Rf2Tele = rF2Telemetry.from_buffer(self._rf2_tele)
        self._rf2_scor = mmap.mmap(0, ctypes.sizeof(rF2Scoring), "$rFactor2SMMP_Scoring$")
        self.Rf2Scor = rF2Scoring.from_buffer(self._rf2_scor)
        self._rf2_ext = mmap.mmap(0, ctypes.sizeof(rF2Extended), "$rFactor2SMMP_Extended$")
        self.Rf2Ext = rF2Extended.from_buffer(self._rf2_ext)

    ###########################################################
    # Access functions
    def isRF2running(self):
        """
        True: rF2 is running and the memory map is loaded
        """
        version = Cbytestring2Python(self.Rf2Ext.mVersion)
        # 2019/04/23:  3.5.0.9
        return version != ''

    def isTrackLoaded(self):
        """
        True: rF2 is running and the track is loaded
        """
        started = self.Rf2Ext.mSessionStarted
        return started != 0

    def isOnTrack(self):
        """
        True: rF2 is running and the player is on track
        """
        realtime = self.Rf2Ext.mInRealtimeFC
        ret = realtime != 0
        return realtime != 0

    def isAiDriving(self):
        """
        True: rF2 is running and the player is on track
        """
        return self.Rf2Scor.mVehicles[0].mControl == 1  # who's in control: -1=nobody (shouldn't get this), 0=local player, 1=local AI, 2=remote, 3=replay (shouldn't get this)
        # didn't work self.Rf2Ext.mPhysics.mAIControl

    def playersVehicleTelemetry(self):
      # Get the variable for the player's vehicle
      return self.Rf2Tele.mVehicles[0]

    def playersVehicleScoring(self):
      # Get the variable for the player's vehicle
      return self.Rf2Scor.mVehicles[0]

    def close(self):
      # This didn't help with the errors
      try:
        self._rf2_tele.close()
        self._rf2_scor.close()
        self._rf2_ext.close()
      except BufferError: # "cannot close exported pointers exist"
        pass

    def __del__(self):
        self.close()

def Cbytestring2Python(bytestring):
    """
    length is size of bytestring buffer
    version = ''.join(chr(i) for i in bytestring[0:length]).rstrip('\0')
    version2 = bytes(bytestring[0:length]).partition(b'\0')[0]
    version3 = bytes(bytestring[0:length]).decode()
    """
    return bytes(bytestring).partition(b'\0')[0].decode().rstrip()

if __name__ == '__main__':
    # Example usage
    info = SimInfo()
    clutch = info.playersVehicleTelemetry().mUnfilteredClutch # 1.0 clutch down, 0 clutch up
    info.playersVehicleTelemetry().mGear = 1
    gear   = info.playersVehicleTelemetry().mGear  # -1 to 6
    assert info.playersVehicleTelemetry().mGear == 1
    info.playersVehicleTelemetry().mGear = 2
    assert info.playersVehicleTelemetry().mGear == 2
    gear   = info.playersVehicleTelemetry().mGear  # -1 to 6
    info.playersVehicleTelemetry().mGear = 1
    assert info.playersVehicleTelemetry().mGear == 1

    driver = Cbytestring2Python(playersVehicleScoring().mDriverName)
    print('%s Gear: %d, Clutch position: %d' % (driver, gear, clutch))

    vehicleName = Cbytestring2Python(playersVehicleScoring().mVehicleName)
    trackName = Cbytestring2Python(info.Rf2Scor.mScoringInfo.mTrackName)
    vehicleClass = Cbytestring2Python(playersVehicleScoring().mVehicleClass)
    
    started = info.Rf2Ext.mSessionStarted
    realtime = info.Rf2Ext.mInRealtimeFC
    ai = info.isAiDriving()

    version = Cbytestring2Python(info.Rf2Ext.mVersion)
    # 2019/04/23:  3.5.0.9

    if info.isRF2running():
      print('Memory map is loaded')
    else:
      print('Memory map is not loaded')

    if info.isTrackLoaded():
      trackName = Cbytestring2Python(info.Rf2Scor.mScoringInfo.mTrackName)
      print('%s is loaded' % trackName)
    else:
      print('Track is not loaded')

    if info.isOnTrack():
      driver = Cbytestring2Python(playersVehicleScoring().mDriverName)
      print('Driver "%s" is on track' % driver)
    else:
      print('Driver is not on track')


    pass
