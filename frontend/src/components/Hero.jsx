import React from 'react';
import { ArrowRight, Info } from 'lucide-react';
import VoterBoxicon from "/picture/Mascot.png";

const Hero = ({ onEnterDApp }) => (
  <div className="hero centre h-fit w-fit flex flex-col min-[970px]:flex-row items-center justify-center px-4">
    <div className="p-8 sm:w-1/2">
      <h1 className="text-4xl font-bold mb-4">Welcome Voter</h1>
      <p className="text-wrap md:text-nowrap text-xl mb-8">Vote for yourself, for future and for the nation.</p>
      <div className="flex flex-col items-center md:flex-row">
        <button onClick={onEnterDApp} className="bg-green-500 hover:bg-green-600 text-white font-bold py-3 px-6 rounded-full flex items-center text-nowrap">
          Enter DApp
          <ArrowRight className="ml-2" size={20} />
        </button>
        <div className="p-2"></div>
        <button className="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-3 px-6 rounded-full flex items-center text-nowrap">
          Learn More
          <Info className="ml-2" size={20} />
        </button>
      </div>
    </div>
    {/* <div className="px-20 py-4"></div> */}
    <div className="min-[970px]:size-1/3">
      <img src={VoterBoxicon} alt="Crypto DApp Illustration" className="" />
    </div>
  </div>
);

export default Hero;