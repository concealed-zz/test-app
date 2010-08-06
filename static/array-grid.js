Ext.onReady(function(){

var menuStore = new Ext.data.JsonStore({
        url: 'getPages',
        fields: ['title', 'content']
    });
    menuStore.load();

    var menuListView = new Ext.list.ListView({
        store: menuStore,
        multiSelect: true,
        emptyText: 'No images to display',
        reserveScrollOffset: true,
		//click:addTab(),
        columns: [{
            header: 'Page',
            width: 1,
            dataIndex: 'title'
        }]
    });
	


var viewport = new Ext.Viewport({
            layout: 'border',
			id: 'viewport',
            items: [
            // create instance immediately
            new Ext.BoxComponent({
                region: 'north',
                height: 32, // give north and south regions a height
                autoEl: {
                    tag: 'div',
                    html:'<p>north - generally for menus, toolbars and/or advertisements</p>'
                }
            }), {
                // lazily created panel (xtype:'panel' is default)
                region: 'south',
                contentEl: 'south',
                split: true,
                height: 100,
                minSize: 100,
                maxSize: 200,
                collapsible: true,
                title: 'South',
                margins: '0 0 0 0'
            }, {
                region: 'east',
                title: 'East Side',
				id: 'east',
                collapsible: true,
                split: true,
                width: 225, // give east and west regions a width
                minSize: 175,
                maxSize: 400,
                margins: '0 5 0 0',
                layout: 'fit', // specify layout manager for items
                items:            // this TabPanel is wrapped by another Panel so the title will be applied
                new Ext.TabPanel({
                    border: false, // already wrapped so don't add another border
                    activeTab: 1, // second tab initially active
					id: 'centerTabs',
                    tabPosition: 'bottom',
                    items: [{
                        html: '<p>A TabPanel component can be a region.</p>',
                        title: 'A Tab',
                        autoScroll: true
                    }, new Ext.grid.PropertyGrid({
                        title: 'Property Grid',
                        closable: true,
                        source: {
                            "(name)": "Properties Grid",
                            "grouping": false,
                            "autoFitColumns": true,
                            "productionQuality": false,
                            "created": new Date(Date.parse('10/15/2006')),
                            "tested": false,
                            "version": 0.01,
                            "borderWidth": 1
                        }
                    })]
                })
            }, {
                region: 'west',
                id: 'west-panel', // see Ext.getCmp() below
                title: 'West',
                split: true,
                width: 100,
                minSize: 175,
                maxSize: 400,
                collapsible: true,
                margins: '0 0 0 5',
                layout: {
                    type: 'fit'
                },
				items: menuListView
            },
            // in this instance the TabPanel is not wrapped by another panel
            // since no title is needed, this Panel is added directly
            // as a Container
            new Ext.TabPanel({
                region: 'center', // a center region is ALWAYS required for border layout
				id: 'center-panel',
                deferredRender: false,
                activeTab: 0,     // first tab initially active
                items: [{
                    contentEl: 'center1',
                    title: 'Close Me',
                    closable: true,
                    autoScroll: true
                }, {
                    contentEl: 'center2',
                    title: 'Center Panel',
                    autoScroll: true
                }]
            })]
        });
// get a reference to the HTML element with id "hideit" and add a click listener to it 
        menuListView.on('click', function(){
		var array = menuListView.getSelectedRecords();
            // get a reference to the Panel that was created with id = 'west-panel' 
            var w = Ext.getCmp('center-panel');
            // expand or collapse that Panel based on its collapsed property state
            w.add({
            title: array[0].data.title,
            iconCls: 'tabs',
            html: array[0].data.content,
                    
            closable:true
        }).show();
        });

function addTab(){
      
    }

		
		});