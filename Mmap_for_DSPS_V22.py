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

# sbyte = ctypes.c_byte
# byte = ctypes.c_ubyte

class rF2Wheel(ctypes.Structure):
    _pack_ = 4
    _fields_ = [
        ('mSuspensionDeflection', ctypes.c_double),
        ('mRideHeight', ctypes.c_double),
        ('mSuspForce', ctypes.c_double),
        ('mBrakeTemp', ctypes.c_double),
        ('mBrakePressure', ctypes.c_double),
        ('mRotation', ctypes.c_double),
        ('mLateralPatchVel', ctypes.c_double),
        ('mLongitudinalPatchVel', ctypes.c_double),
        ('mLateralGroundVel', ctypes.c_double),
        ('mLongitudinalGroundVel', ctypes.c_double),
        ('mCamber', ctypes.c_double),
        ('mLateralForce', ctypes.c_double),
        ('mLongitudinalForce', ctypes.c_double),
        ('mTireLoad', ctypes.c_double),
        ('mGripFract', ctypes.c_double),
        ('mPressure', ctypes.c_double),
        ('mTemperature', ctypes.c_double*3),
        ('mWear', ctypes.c_double),
        ('mTerrainName', ctypes.c_ubyte*16),
        ('mSurfaceType', ctypes.c_ubyte),
        ('mFlat', ctypes.c_ubyte),
        ('mDetached', ctypes.c_ubyte),
        ('mVerticalTireDeflection', ctypes.c_double),
        ('mWheelYLocation', ctypes.c_double),
        ('mToe', ctypes.c_double),
        ('mTireCarcassTemperature', ctypes.c_double),
        ('mTireInnerLayerTemperature', ctypes.c_double*3),
        ('mExpansion', ctypes.c_ubyte*24),
    ]


class rF2VehicleTelemetry(ctypes.Structure):
    _pack_ = 4
    _fields_ = [
        ('mID', ctypes.c_int),
        ('mDeltaTime', ctypes.c_double),
        ('mElapsedTime', ctypes.c_double),
        ('mLapNumber', ctypes.c_int),
        ('mLapStartET', ctypes.c_double),
        ('mVehicleName', ctypes.c_ubyte*64), # byte
        ('mTrackName', ctypes.c_ubyte*64), # byte
        ('mPos', rF2Vec3),
        ('mLocalVel', rF2Vec3),
        ('mLocalAccel', rF2Vec3),
        ('mOri', rF2Vec3*3),
        ('mLocalRot', rF2Vec3),
        ('mLocalRotAccel', rF2Vec3),
        ('mGear', ctypes.c_int),
        ('mEngineRPM', ctypes.c_double),
        ('mEngineWaterTemp', ctypes.c_double),
        ('mEngineOilTemp', ctypes.c_double),
        ('mClutchRPM', ctypes.c_double),
        ('mUnfilteredThrottle', ctypes.c_double),
        ('mUnfilteredBrake', ctypes.c_double),
        ('mUnfilteredSteering', ctypes.c_double),
        ('mUnfilteredClutch', ctypes.c_double),
        ('mFilteredThrottle', ctypes.c_double),
        ('mFilteredBrake', ctypes.c_double),
        ('mFilteredSteering', ctypes.c_double),
        ('mFilteredClutch', ctypes.c_double),
        ('mSteeringShaftTorque', ctypes.c_double),
        ('mFront3rdDeflection', ctypes.c_double),
        ('mRear3rdDeflection', ctypes.c_double),
        ('mFrontWingHeight', ctypes.c_double),
        ('mFrontRideHeight', ctypes.c_double),
        ('mRearRideHeight', ctypes.c_double),
        ('mDrag', ctypes.c_double),
        ('mFrontDownforce', ctypes.c_double),
        ('mRearDownforce', ctypes.c_double),
        ('mFuel', ctypes.c_double),
        ('mEngineMaxRPM', ctypes.c_double),
        ('mScheduledStops', ctypes.c_ubyte), # byte
        ('mOverheating', ctypes.c_ubyte), # byte
        ('mDetached', ctypes.c_ubyte), # byte
        ('mHeadlights', ctypes.c_ubyte), # byte
        ('mDentSeverity', ctypes.c_ubyte*8), # byte
        ('mLastImpactET', ctypes.c_double),
        ('mLastImpactMagnitude', ctypes.c_double),
        ('mLastImpactPos', rF2Vec3),
        ('mEngineTorque', ctypes.c_double),
        ('mCurrentSector', ctypes.c_int),
        ('mSpeedLimiter', ctypes.c_ubyte), # byte
        ('mMaxGears', ctypes.c_ubyte), # byte
        ('mFrontTireCompoundIndex', ctypes.c_ubyte), # byte
        ('mRearTireCompoundIndex', ctypes.c_ubyte), # byte
        ('mFuelCapacity', ctypes.c_double),
        ('mFrontFlapActivated', ctypes.c_ubyte), # byte
        ('mRearFlapActivated', ctypes.c_ubyte), # byte
        ('mRearFlapLegalStatus', ctypes.c_ubyte), # byte
        ('mIgnitionStarter', ctypes.c_ubyte), # byte
        ('mFrontTireCompoundName', ctypes.c_ubyte*18), # byte
        ('mRearTireCompoundName', ctypes.c_ubyte*18), # byte
        ('mSpeedLimiterAvailable', ctypes.c_ubyte), # byte
        ('mAntiStallActivated', ctypes.c_ubyte), # byte
        ('mUnused', ctypes.c_ubyte*2), # byte
        ('mVisualSteeringWheelRange', ctypes.c_float),
        ('mRearBrakeBias', ctypes.c_double),
        ('mTurboBoostPressure', ctypes.c_double),
        ('mPhysicsToGraphicsOffset', ctypes.c_float*3),
        ('mPhysicalSteeringWheelRange', ctypes.c_float),
        ('mExpansion', ctypes.c_ubyte*152), # byte
        ('mWheels', rF2Wheel*4), # byte
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
        ('mTrackName', ctypes.c_ubyte*64), # byte
        ('mSession', ctypes.c_int),
        ('mCurrentET', ctypes.c_double),
        ('mEndET', ctypes.c_double),
        ('mMaxLaps', ctypes.c_int),
        ('mLapDist', ctypes.c_double),
        ('pointer1', ctypes.c_ubyte*8), # byte
        ('mNumVehicles', ctypes.c_int),
        ('mGamePhase', ctypes.c_ubyte), # byte
        ('mYellowFlagState', ctypes.c_byte), # sbyte
        ('mSectorFlag', ctypes.c_byte*3), # sbyte
        ('mStartLight', ctypes.c_ubyte), # byte
        ('mNumRedLights', ctypes.c_ubyte), # byte
        ('mInRealtime', ctypes.c_ubyte), # byte
        ('mPlayerName', ctypes.c_ubyte*32), # byte
        ('mPlrFileName', ctypes.c_ubyte*64), # byte
        ('mDarkCloud', ctypes.c_double),
        ('mRaining', ctypes.c_double),
        ('mAmbientTemp', ctypes.c_double),
        ('mTrackTemp', ctypes.c_double),
        ('mWind', rF2Vec3),
        ('mMinPathWetness', ctypes.c_double),
        ('mMaxPathWetness', ctypes.c_double),
        ('mExpansion', ctypes.c_ubyte*256), # byte
        ('pointer2', ctypes.c_ubyte*8), # byte
    ]


class rF2VehicleScoring(ctypes.Structure):
    _pack_ = 4
    _fields_ = [
        ('mID', ctypes.c_int),
        ('mDriverName', ctypes.c_ubyte*32), # byte
        ('mVehicleName', ctypes.c_ubyte*64), # byte
        ('mTotalLaps', ctypes.c_short),
        ('mSector', ctypes.c_byte), # sbyte
        ('mFinishStatus', ctypes.c_byte), # sbyte
        ('mLapDist', ctypes.c_double),
        ('mPathLateral', ctypes.c_double),
        ('mTrackEdge', ctypes.c_double),
        ('mBestSector1', ctypes.c_double),
        ('mBestSector2', ctypes.c_double),
        ('mBestLapTime', ctypes.c_double),
        ('mLastSector1', ctypes.c_double),
        ('mLastSector2', ctypes.c_double),
        ('mLastLapTime', ctypes.c_double),
        ('mCurSector1', ctypes.c_double),
        ('mCurSector2', ctypes.c_double),
        ('mNumPitstops', ctypes.c_short),
        ('mNumPenalties', ctypes.c_short),
        ('mIsPlayer', ctypes.c_ubyte),  # byte
        ('mControl', ctypes.c_byte), # sbyte
        ('mInPits', ctypes.c_ubyte), # byte
        ('mPlace', ctypes.c_ubyte), # byte
        ('mVehicleClass', ctypes.c_ubyte*32), # byte
        ('mTimeBehindNext', ctypes.c_double),
        ('mLapsBehindNext', ctypes.c_int),
        ('mTimeBehindLeader', ctypes.c_double),
        ('mLapsBehindLeader', ctypes.c_int),
        ('mLapStartET', ctypes.c_double),
        ('mPos', rF2Vec3),
        ('mLocalVel', rF2Vec3),
        ('mLocalAccel', rF2Vec3),
        ('mOri', rF2Vec3*3),
        ('mLocalRot', rF2Vec3),
        ('mLocalRotAccel', rF2Vec3),
        ('mHeadlights', ctypes.c_ubyte), # byte
        ('mPitState', ctypes.c_ubyte), # byte
        ('mServerScored', ctypes.c_ubyte), # byte
        ('mIndividualPhase', ctypes.c_ubyte), # byte
        ('mQualification', ctypes.c_int),
        ('mTimeIntoLap', ctypes.c_double),
        ('mEstimatedLapTime', ctypes.c_double),
        ('mPitGroup', ctypes.c_ubyte*24),  # byte
        ('mFlag', ctypes.c_ubyte),  # byte
        ('mUnderYellow', ctypes.c_ubyte),  # byte
        ('mCountLapFlag', ctypes.c_ubyte),  # byte
        ('mInGarageStall', ctypes.c_ubyte),  # byte
        ('mUpgradePack', ctypes.c_ubyte*16),  # byte
        ('mExpansion', ctypes.c_ubyte*60),  # byte
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
        ('mTractionControl', ctypes.c_ubyte),
        ('mAntiLockBrakes', ctypes.c_ubyte),
        ('mStabilityControl', ctypes.c_ubyte),
        ('mAutoShift', ctypes.c_ubyte),
        ('mAutoClutch', ctypes.c_ubyte),
        ('mInvulnerable', ctypes.c_ubyte),
        ('mOppositeLock', ctypes.c_ubyte),
        ('mSteeringHelp', ctypes.c_ubyte),
        ('mBrakingHelp', ctypes.c_ubyte),
        ('mSpinRecovery', ctypes.c_ubyte),
        ('mAutoPit', ctypes.c_ubyte),
        ('mAutoLift', ctypes.c_ubyte),
        ('mAutoBlip', ctypes.c_ubyte),
        ('mFuelMult', ctypes.c_ubyte),
        ('mTireMult', ctypes.c_ubyte),
        ('mMechFail', ctypes.c_ubyte),
        ('mAllowPitcrewPush', ctypes.c_ubyte),
        ('mRepeatShifts', ctypes.c_ubyte),
        ('mHoldClutch', ctypes.c_ubyte),
        ('mAutoReverse', ctypes.c_ubyte),
        ('mAlternateNeutral', ctypes.c_ubyte),
        ('mAIControl', ctypes.c_ubyte),
        ('mUnused1', ctypes.c_ubyte),
        ('mUnused2', ctypes.c_ubyte),
        ('mManualShiftOverrideTime', ctypes.c_float),
        ('mAutoShiftOverrideTime', ctypes.c_float),
        ('mSpeedSensitiveSteering', ctypes.c_float),
        ('mSteerRatioSpeed', ctypes.c_float),
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
        ('mInRealtimeFC', ctypes.c_ubyte),
        ('mMultimediaThreadStarted', ctypes.c_ubyte),
        ('mSimulationThreadStarted', ctypes.c_ubyte),
        ('mSessionStarted', ctypes.c_ubyte),
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

    def close(self):
        self._rf2_tele.close()
        self._rf2_scor.close()
        self._rf2_ext.close()

    def __del__(self):
        self.close()

info = SimInfo()

