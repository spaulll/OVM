import React, { useState, useEffect } from "react";
import { X, CircleArrowLeft } from "lucide-react";
import { fetchUsers } from "@/utils/getDetails";
import { ethers } from "ethers";
import Message from "@/components/AfterVoteMessage";
import LoadingModal from "@/components/LoadingModal";
import AdminUserCard from "@/components/Admin/AdminUserCard";
import { dummyUsers } from "@/utils/testData";

const AdminUserControlsPage = ({ wallet, onRemove, onClose, onBack }) => {
  const [Users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showUserRemovedMessage, setShowUserRemovedMessage] = useState(false);
  const [messageData, setMessageData] = useState("");
  const [txHash, setTxHash] = useState("");

  useEffect(() => {
    const loadUsers = async () => {
      setLoading(true);
      try {
        const fetchedUsers = await fetchUsers(wallet);
        setUsers(fetchedUsers);
        // setUsers(dummyUsers); // Using Dummy data for testing
      } catch (err) {
        setError("Failed to load Users. Please try again later.");
        //console.error(err);
      } finally {
        setLoading(false);
      }
    };
    loadUsers();
  }, [wallet]);

  if (loading)
    return (
      <div>
        <LoadingModal
          modalVisible={loading}
          task="Loading Users..."
          onClose={onClose}
        />
      </div>
    );
  if (error)
    return (
      <div>
        <div className="loading-modal-overlay" onClick={onClose}>
          <div className="loading-modal">
            <p className="text-red-500">{error}</p>
          </div>
          <button onClick={onClose} className="relative right-0 top-[-3rem]">
            <X
              className="bg-red-500 hover:bg-red-600 text-white hover:text-gray-700 rounded-full"
              size={24}
            />
          </button>
        </div>
      </div>
    );

    return (
      <div className="container mx-auto px-4 py-8 relative">
        {/* Back Button */}
        <div className="relative flex justify-start items-start">
          <button
            className="relative left-0 h-10 w-10 text-black-500 hover:text-gray-500" // Adjusted the positioning
            onClick={onBack}
          >
            <CircleArrowLeft size={34} strokeWidth={1.75} />
          </button>
        </div>
    
        {/* Title */}
        <h2 className="text-3xl font-bold mb-8 text-center">Users:</h2>
    
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute right-4 top-4" // Positioned close button at the top right corner
        >
          <X
            className="bg-red-500 hover:bg-red-600 text-white hover:text-gray-700 rounded-full"
            size={24}
          />
        </button>
    
        {/* User Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4 gap-6">
          {Users.map((user) => (
            <AdminUserCard key={user.id} user={user} onRemove={onRemove} />
          ))}
        </div>
    
        {/* User Removed Message */}
        {showUserRemovedMessage && (
          <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
            <Message
              data={messageData}
              txhash={txHash ? `${txHash}` : null}
              onClose={() => setShowUserRemovedMessage(false)}
            />
          </div>
        )}
      </div>
    );    
};

export default AdminUserControlsPage;
