import { useContext } from 'react';
import BotContext from '../contexts/BotContext';

const useBot = () => useContext(BotContext);

export default useBot;
