import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DairyCowListComponent } from './dairy-cow-list.component';

describe('DairyCowListComponent', () => {
  let component: DairyCowListComponent;
  let fixture: ComponentFixture<DairyCowListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DairyCowListComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DairyCowListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
