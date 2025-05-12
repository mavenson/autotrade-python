class Menu:
    def __init__(self):
        self._menu_dict =   {

                            # Need to add Header Feature, gives quick relevant readout specific to given menu.


                            # Menu Format is one dict containing the name of the menu in the key, and the menu items
                            # as well as additional data in a list as the element.
                            # The first item of the list refers to it's parent menu to facilitate
                            # going 'back' in the menu. Always sets back to 0.
                            # The second item of the list refers to which header, if any to apply.
                            # The rest of list contains menu items.
                            # Storing this data in a separate file may be tidier, for now, easier to modify here.


                            # Layer 1 Menus (Main Menu)
            
                            'Main Menu':['null',
                            'Manual Trading',
                            'Automation',
                            'Market Scanner',
                            'Back Testing',
                            'Performance Tracking',
                            'Display Active Tasks'],


                            # Layer 2 Menus
                            
                            'Manual Trading':
                            ['Main Menu','Analysis',
                            'Custom Order',
                            'Risk/Reward Strict Order',
                            'Risk/Reward Ratio',
                            'Set Position Size',
                            'Select Instrument',
                            'View Orders for Selected Instrument',
                            'Cancel All Orders for Selected Instrument',
                            'Cancel Specific Order',
                            'Cancel and Replace with Modified Order'],
                            'Automation':
                            ['Main Menu','Automatic',
                            'Custom (w/ Advisory)'],
                            'Market Scanner':
                            ['Main Menu','All Instruments',
                            'Aggregated Instrument Readouts',
                            'Edit Instrument Aggregates',
                            'Specific Instrument Readout'],
                            'Back Testing':
                            ['Main Menu','Create New Back Test',
                            'Data Inventory and Integrity',
                            'Back Test Records'],
                            'Performance Tracking':
                            ['Main Menu','Overall Performance',
                            'Instrument Strategy Performance',
                            'Portfolio Strategy Performance'],
                            'Display Active Tasks':
                            ['Main Menu','Cancel Order or Strategy'],

                            # Layer 3 Menus
                            
                            'Custom Order':
                            ['Manual Trading','Set Buy Limit at Custom Price',
                            'Set Sell Limit at Custom Price',
                            'Stop Loss at Custom Price',
                            'Set Buy Market above Entry Order at Custom Price', 
                            'Buy Market',
                            'Sell Market'],
                            'Risk/Reward Strict Order':
                           ['Manual Trading','Place Bullish Trigger at x price to Place Limit Order in Risk/Reward Ratio Based on trigger price.',
                            'Place Bearish Trigger at x price to Place Limit Order in Risk/Reward Ratio Based on Trigger Price.',
                            'Place Bullish Limit Order and Stop Loss in Risk/Reward Ratio Based on Current Price.',
                            'Place Bearish Limit Order and Stop Loss in Risk/Reward Ratio Based on Current Price'],
                            'Risk/Reward Ratio':
                           ['Manual Trading','Custom Ratio','Optimization Mode'],
                            'Set Position Size':
                           ['Manual Trading','Custom Position Size',
                            'Max Position Size',
                            'Optimization Mode'],
                            'Select Instrument':
                           ['Manual Trading','Select Instrument',
                            'From Full List',
                            'By Exchange',
                            'From Scanner Favorites'],
                            'Automatic':
                           ['Automation','Display Active Portfolio Strategies',
                            'Toggle Auto Portfolio On/Off',
                            'Deploy Auto Portfolio Strategy',
                            'Dismiss Auto Portfolio Strategy',
                            'Portfolio Strategy Settings'],
                            'Custom (w/ Advisory)':
                           ['Automation','Display Active Instrument Strategies', 
                            'Deploy Instrument Strategy',
                            'Dismiss Instrument Strategy',
                            'Address Advisories (Generated by Automatic Mode)'],
                            'Edit Instrument Aggregates':
                           ['Market Scanner','Create Aggregate',
                            'Delete Aggregate',
                            'Edit Aggregate'],
                            'Specific Instrument Readout':
                           ['Market Scanner','Last Instrument Viewed',
                            'Enter Instrument Symbol',
                            'Select From Favorites',
                            'Add Favorite',
                            'Delete Favorite',
                            'Select from All Available Instruments'],
                            'Create a New Back Test':
                           ['Back Testing','Test Portfolio Strategies',
                            'Test Instrument Strategies,'],
                            'Data Integrity and Inventory':
                           ['Back Testing','Begin Scrubbing Data from Oldest to Newest',
                            'Specify a Time Period to Scrub'],
                            'Back Test Records':
                           ['Back Testing','Display Most Recent Back Test Results',
                            'Browse Older Results'],
                            'Instrument Strategy Performance':
                           ['Performance Tracking','Sort by (inst)',
                            'View Individual Strategies'],
                            'Portfolio Strategy Performance':
                           ['Performance Tracking','Sort by (port)',
                            'View Individual Strategies'],

                            # Layer 4 Menus

                            'Deploy Auto Portfolio Strategy':
                           ['Automatic','Modify Settings?',
                            'Save Template',
                            'Deploy',],
                            'Dismiss Auto Portfolio Strategy':
                           ['Automatic','Auto Exit Positions?',
                            'Cease All Activity'],
                            'Deploy Instrument Strategy':
                           ['Custom (w/ Advisory)','Choose Custom Strategy for Instrument',
                            'Suggest Best Strategy'],
                            'Dismiss Instrument Strategy':
                           ['Custom (w/ Advisory)','Auto Exit Position?',
                            'Cease All Activity Now'],
                            'Address Advisories (Generated by Automatic Mode)':
                           ['Custom (w/ Advisory)','Go Through All From Most Confident',
                            'Enter Advisory ID to Begin From',
                            'Enter Advisory IDs to Address',],
                            'Browse Older Results':
                           ['Back Test Records','Next',
                            'Previous'],
                            'Sort by (inst)':
                           ['Instrument Strategy Performance','Overall Accuracy',
                            'Profit in Practice',
                            'Total Profit in Back Tests',
                            'Edge in Practice',
                            'Edge in Back Tests',
                            'Time since First Use',
                            'Time since Settings Adjusted',
                            'Disparity Between Back Tests'],
                            'Sort by (port)':
                           ['Portfolio Strategy Performance','Overall Accuracy',
                            'Profit in Practice',
                            'Total Profit in Back Tests',
                            'Edge in Practice',
                            'Edge in Back Tests',
                            'Time since First Use',
                            'Time since Settings Adjusted',
                            'Disparity Between Back Tests'],

                            # Layer 5 Menus

                             'Choose Custom Strategy for Instrument':
                            ['Modify Settings?',
                             'Save Template',
                             'Deploy'],
                            'Suggest Best Strategy':
                            ['Modify Settings?',
                             'Save Template',
                             'Deploy'],
                             'Go Through All From Most Confident':
                            ['Execute',
                             'Skip',
                             'Modify and Execute',
                             'Reject'],
                             'Enter Advisory ID to Begin From':
                            ['Next',
                             'Previous',
                             'Execute',
                             'Modify and Execute',
                             'Reject'],
                             'Enter Advisory IDs to Address':
                            ['Next',
                             'Previous',
                             'Execute',
                             'Modify and Execute',
                             'Reject']
                             }

    def genMenu(self, item_list):
        valid_choices = [e for e in range(len(item_list)+1)]
        while True:
            # Enter Header Generating Function Here
            counter = 1
            for e in item_list[1:]:    ## Change to start from 3rd or [2:] to implement header feature
                print('%s.) %s:'%(counter,e))
                counter += 1
            if item_list[0] == 'null':
                print('%s.) %s:'%(0,'Exit'))
            else:    
                print('%s.) %s:'%(0,'Back'))
                                                ## Printing of menu finished
            user_input = input('\nEnter Selection: ')
            user_input = int(user_input)
            while user_input not in valid_choices:
                user_input = input('\nInvalid Selection, Try Again: ')
                user_input = int(user_input)
            if user_input == 0 and item_list[0] != 'null':

                self.genMenu(self._menu_dict[item_list[user_input]])
            elif user_input == 0 and item_list[0] == 'null':
                exit()
            else:
                try:
                    self.genMenu(self._menu_dict[item_list[user_input]])
                except:
                    print('\nEnd Point at %s.\n'%(item_list[user_input]))
                    
    def launch(self):
        self.genMenu(self._menu_dict['Main Menu'])
        
m = Menu()
m.launch()
        
        
